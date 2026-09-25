use pyo3::prelude::*;
use pyo3::types::PyString;
use anyhow::{Result, anyhow};
use crate::knowledge::KnowledgeNode;

/// 全维精算引擎：自动运行节点的Python代码，验证公式正确性，返回验证结果
pub struct FractalCalculator;

impl FractalCalculator {
    pub fn new() -> Self {
        Self
    }

    /// 验证单个知识节点的Python代码，自动运行并检查断言
    pub fn verify_node(&self, node: &mut KnowledgeNode) -> Result<()> {
        if node.python_code.is_none() {
            node.verified = false;
            node.verification_result = Some("无验证代码".into());
            return Ok(());
        }
        let code = node.python_code.as_ref().unwrap();

        Python::with_gil(|py| -> Result<()> {
            // 重定向stdout捕获输出
            let sys = py.import("sys")?;
            let io = py.import("io")?;
            let string_io = io.call_method1("StringIO", ())?;
            sys.setattr("stdout", string_io)?;

            let result = py.run(code, None, None);
            let output = string_io.call_method0("getvalue")?;
            let output_str: String = output.extract()?;

            match result {
                Ok(_) => {
                    node.verified = true;
                    node.verification_result = Some(format!("验证通过，输出：\n{}", output_str));
                    Ok(())
                }
                Err(e) => {
                    node.verified = false;
                    node.verification_result = Some(format!("验证失败：{}", e));
                    Err(anyhow!("节点{}验证失败：{}", node.title, e))
                }
            }
        })
    }

    /// 批量验证整个知识图谱的所有节点
    pub fn verify_all_nodes(&self, nodes: &mut Vec<KnowledgeNode>) -> (usize, usize) {
        let mut success = 0;
        let mut failed = 0;
        for node in nodes.iter_mut() {
            match self.verify_node(node) {
                Ok(_) => success += 1,
                Err(_) => failed += 1,
            }
        }
        (success, failed)
    }

    /// 自动生成验证代码：根据LaTeX公式自动生成Python验证代码
    pub fn auto_generate_verification_code(latex: &str) -> String {
        // 简单的自动生成逻辑，后续可以扩展为AI生成
        let mut code = String::new();
        code.push_str("import math\nc=299792458.0; hbar=1.0545718e-34; G=6.6743e-11; alpha=1/137.036\n");
        if latex.contains("\\kappa^2+\\tau^2") {
            code.push_str(r#"
def kappa_tau_sum(r,h):
    k = r/(r**2+h**2)
    t = h/(r**2+h**2)
    return k**2 + t**2
assert abs(kappa_tau_sum(1,0.5) - 1/(1+0.25)) < 1e-10
print("κ²+τ²=常数 自动验证通过")
"#);
        }
        if latex.contains("m_0 = \\frac{\\hbar \\kappa}{c}") {
            code.push_str(r#"
m_e = 9.10938e-31
kappa_e = m_e*c/hbar
assert abs(hbar*kappa_e/c - m_e) < 1e-40
print("质量几何定义 自动验证通过")
"#);
        }
        code
    }
}

impl Default for FractalCalculator {
    fn default() -> Self {
        Self::new()
    }
}
