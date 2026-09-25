mod knowledge;
mod calculator;
mod inference;

use knowledge::FractalKnowledgeGraph;
use calculator::FractalCalculator;
use inference::InferenceEngine;
use std::fs;
use serde_json;

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    env_logger::init();
    println!("==============================================");
    println!("  全维分形知识自动演化引擎 v0.1.0");
    println!("  算法联盟最高权限 | 0·1·∞ 全域螺旋统一场");
    println!("==============================================");

    // 1. 初始化分形知识图谱，加载核心公理
    println!("\n[1/5] 初始化核心公理知识图谱...");
    let mut kg = FractalKnowledgeGraph::new();
    println!("  已加载{}个核心公理", kg.axioms.len());

    // 2. 自动推理推导新公式
    println!("\n[2/5] 自动推理推导核心公式...");
    let inference = InferenceEngine::new();
    let new_formulas = inference.derive_new_formulas(&mut kg);
    println!("  自动推导出{}个核心公式", new_formulas.len());

    // 3. 自动精算验证所有节点
    println!("\n[3/5] 自动Python精算验证所有公式...");
    let calculator = FractalCalculator::new();
    let mut all_nodes: Vec<_> = kg.graph.node_indices().map(|i| kg.graph[i].clone()).collect();
    let (success, failed) = calculator.verify_all_nodes(&mut all_nodes);
    // 把验证结果写回图
    for (i, idx) in kg.graph.node_indices().enumerate() {
        kg.graph[idx] = all_nodes[i].clone();
    }
    println!("  验证完成：成功{}个，失败{}个", success, failed);

    // 4. 分形扩展知识
    println!("\n[4/5] 分形扩展知识图谱...");
    let new_expand = inference.random_fractal_expand(&mut kg, 10);
    println!("  分形扩展生成{}个新知识节点", new_expand.len());
    println!("  当前知识图谱总节点数：{}", kg.graph.node_count());
    println!("  当前知识图谱总边数：{}", kg.graph.edge_count());

    // 5. 导出知识图谱为JSON
    println!("\n[5/5] 导出知识图谱到output/knowledge_graph.json...");
    fs::create_dir_all("output")?;
    let export = serde_json::to_string_pretty(&all_nodes)?;
    fs::write("output/knowledge_graph.json", export)?;

    // 自动生成示例小说
    println!("\n自动生成示例科幻小说到output/超宇宙文明.md...");
    let novel = inference.generate_fiction(&kg, "超宇宙文明");
    fs::write("output/超宇宙文明.md", &novel.content)?;

    // 自动生成示例代码
    println!("自动生成反重力Python代码到output/anti_gravity.py...");
    let anti_g_node = &kg.graph[new_formulas[3]];
    let code = inference.generate_code(anti_g_node, "python");
    fs::write("output/anti_gravity.py", code)?;

    println!("\n==============================================");
    println!("  引擎启动完成！知识图谱已自动演化完成");
    println!("  输出文件位于output/目录：");
    println!("    - knowledge_graph.json：完整知识图谱");
    println!("    - 超宇宙文明.md：自动生成的科幻小说");
    println!("    - anti_gravity.py：自动生成的反重力代码");
    println!("==============================================");

    Ok(())
}
