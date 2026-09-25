//! # 知识图谱模块
//!
//! 实现公理3：关联关系加权有向图
//! 基于petgraph实现加权有向图，支持邻接矩阵、关联度计算、图拉普拉斯等

use nalgebra::DMatrix;
use petgraph::graph::{DiGraph, NodeIndex};
use petgraph::visit::EdgeRef;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;

pub use operator_core::Result;

/// 知识图谱节点
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct KnowledgeNode {
    pub id: String,
    pub label: String,
    pub properties: serde_json::Value,
    pub embedding: Option<Vec<f64>>,
}

/// 知识图谱边
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct KnowledgeEdge {
    pub source: String,
    pub target: String,
    pub weight: f64,
    pub relation_type: String,
    pub properties: serde_json::Value,
}

/// 知识图谱
#[derive(Debug, Clone)]
pub struct KnowledgeGraph {
    graph: DiGraph<KnowledgeNode, f64>,
    node_map: HashMap<String, NodeIndex>,
    damping_factor: f64,
}

impl KnowledgeGraph {
    pub fn new() -> Self {
        Self {
            graph: DiGraph::new(),
            node_map: HashMap::new(),
            damping_factor: 0.85,
        }
    }

    pub fn with_damping(damping: f64) -> Self {
        Self {
            graph: DiGraph::new(),
            node_map: HashMap::new(),
            damping_factor: damping,
        }
    }

    /// 添加节点
    pub fn add_node(&mut self, node: KnowledgeNode) -> NodeIndex {
        let id = node.id.clone();
        let idx = self.graph.add_node(node);
        self.node_map.insert(id, idx);
        idx
    }

    /// 添加边
    pub fn add_edge(&mut self, edge: KnowledgeEdge) -> Result<()> {
        let source = self
            .node_map
            .get(&edge.source)
            .ok_or_else(|| anyhow::anyhow!("源节点不存在: {}", edge.source))?;
        let target = self
            .node_map
            .get(&edge.target)
            .ok_or_else(|| anyhow::anyhow!("目标节点不存在: {}", edge.target))?;
        self.graph.add_edge(*source, *target, edge.weight);
        Ok(())
    }

    /// 获取节点
    pub fn get_node(&self, id: &str) -> Option<&KnowledgeNode> {
        self.node_map.get(id).map(|idx| &self.graph[*idx])
    }

    /// 获取节点数
    pub fn node_count(&self) -> usize {
        self.graph.node_count()
    }

    /// 获取边数
    pub fn edge_count(&self) -> usize {
        self.graph.edge_count()
    }

    /// 构建邻接矩阵
    pub fn adjacency_matrix(&self) -> DMatrix<f64> {
        let n = self.node_count();
        let mut adj = DMatrix::zeros(n, n);
        for edge in self.graph.edge_references() {
            let i = edge.source().index();
            let j = edge.target().index();
            adj[(i, j)] = *edge.weight();
        }
        adj
    }

    /// 构建度矩阵
    pub fn degree_matrix(&self) -> DMatrix<f64> {
        let n = self.node_count();
        let adj = self.adjacency_matrix();
        let mut deg = DMatrix::zeros(n, n);
        for i in 0..n {
            let row_sum: f64 = (0..n).map(|j| adj[(i, j)]).sum();
            deg[(i, i)] = row_sum;
        }
        deg
    }

    /// 构建拉普拉斯矩阵 L = D - A
    pub fn laplacian_matrix(&self) -> DMatrix<f64> {
        self.degree_matrix() - self.adjacency_matrix()
    }

    /// 计算k步关联度
    pub fn k_step_relevance(&self, source: &str, target: &str, k: usize) -> Result<f64> {
        let source_idx = self
            .node_map
            .get(source)
            .ok_or_else(|| anyhow::anyhow!("源节点不存在: {}", source))?;
        let target_idx = self
            .node_map
            .get(target)
            .ok_or_else(|| anyhow::anyhow!("目标节点不存在: {}", target))?;

        let adj = self.adjacency_matrix();
        let a_k = adj.pow(k as u32);
        let frobenius_norm = a_k.norm();

        if frobenius_norm < 1e-15 {
            return Ok(0.0);
        }

        Ok(a_k[(source_idx.index(), target_idx.index())] / frobenius_norm)
    }

    /// 计算全步关联度（带衰减）
    pub fn total_relevance(&self, source: &str, target: &str) -> Result<f64> {
        let source_idx = self
            .node_map
            .get(source)
            .ok_or_else(|| anyhow::anyhow!("源节点不存在: {}", source))?;
        let target_idx = self
            .node_map
            .get(target)
            .ok_or_else(|| anyhow::anyhow!("目标节点不存在: {}", target))?;

        let n = self.node_count();
        let adj = self.adjacency_matrix();
        let alpha = self.damping_factor;

        // (I - alpha*A)^(-1) = sum_{k=0}^\infty (alpha*A)^k
        let identity = DMatrix::identity(n, n);
        let matrix = &identity - &(&adj * alpha);
        let inv = matrix
            .try_inverse()
            .ok_or_else(|| anyhow::anyhow!("矩阵不可逆"))?;

        Ok(inv[(source_idx.index(), target_idx.index())])
    }

    /// PageRank算法
    pub fn pagerank(&self, iterations: usize) -> HashMap<String, f64> {
        let n = self.node_count();
        if n == 0 {
            return HashMap::new();
        }

        let alpha = self.damping_factor;
        let adj = self.adjacency_matrix();
        let mut deg = DMatrix::zeros(n, n);
        for i in 0..n {
            let row_sum: f64 = (0..n).map(|j| adj[(i, j)]).sum();
            if row_sum > 1e-15 {
                deg[(i, i)] = 1.0 / row_sum;
            }
        }

        let transition = &deg * &adj;
        let mut rank = DMatrix::from_element(n, 1, 1.0 / n as f64);

        for _ in 0..iterations {
            rank = &transition * alpha * &rank
                + DMatrix::from_element(n, 1, (1.0 - alpha) / n as f64);
        }

        let mut result = HashMap::new();
        for (id, idx) in &self.node_map {
            result.insert(id.clone(), rank[(idx.index(), 0)]);
        }
        result
    }

    /// 邻居节点
    pub fn neighbors(&self, id: &str) -> Result<Vec<(String, f64)>> {
        let idx = self
            .node_map
            .get(id)
            .ok_or_else(|| anyhow::anyhow!("节点不存在: {}", id))?;
        let mut neighbors = Vec::new();
        for edge in self.graph.edges(*idx) {
            let target = &self.graph[edge.target()];
            neighbors.push((target.id.clone(), *edge.weight()));
        }
        Ok(neighbors)
    }

    /// 获取所有节点
    pub fn nodes(&self) -> Vec<&KnowledgeNode> {
        self.graph.node_weights().collect()
    }

    /// 获取所有边
    pub fn edges(&self) -> Vec<KnowledgeEdge> {
        self.graph
            .edge_references()
            .map(|e| {
                let source = &self.graph[e.source()];
                let target = &self.graph[e.target()];
                KnowledgeEdge {
                    source: source.id.clone(),
                    target: target.id.clone(),
                    weight: *e.weight(),
                    relation_type: "related".to_string(),
                    properties: serde_json::json!({}),
                }
            })
            .collect()
    }
}

impl Default for KnowledgeGraph {
    fn default() -> Self {
        Self::new()
    }
}

/// 知识图谱构建算子
pub struct KnowledgeGraphBuilder {
    graph: KnowledgeGraph,
}

impl KnowledgeGraphBuilder {
    pub fn new() -> Self {
        Self {
            graph: KnowledgeGraph::new(),
        }
    }

    pub fn add_node(mut self, id: &str, label: &str) -> Self {
        self.graph.add_node(KnowledgeNode {
            id: id.to_string(),
            label: label.to_string(),
            properties: serde_json::json!({}),
            embedding: None,
        });
        self
    }

    pub fn add_edge(mut self, source: &str, target: &str, weight: f64) -> Self {
        let _ = self.graph.add_edge(KnowledgeEdge {
            source: source.to_string(),
            target: target.to_string(),
            weight,
            relation_type: "related".to_string(),
            properties: serde_json::json!({}),
        });
        self
    }

    pub fn build(self) -> KnowledgeGraph {
        self.graph
    }
}

impl Default for KnowledgeGraphBuilder {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use approx::assert_relative_eq;

    #[test]
    fn test_graph_creation() {
        let mut graph = KnowledgeGraph::new();
        graph.add_node(KnowledgeNode {
            id: "a".to_string(),
            label: "A".to_string(),
            properties: serde_json::json!({}),
            embedding: None,
        });
        graph.add_node(KnowledgeNode {
            id: "b".to_string(),
            label: "B".to_string(),
            properties: serde_json::json!({}),
            embedding: None,
        });
        assert_eq!(graph.node_count(), 2);
        assert_eq!(graph.edge_count(), 0);
    }

    #[test]
    fn test_adjacency_matrix() {
        let graph = KnowledgeGraphBuilder::new()
            .add_node("a", "A")
            .add_node("b", "B")
            .add_edge("a", "b", 1.0)
            .build();

        let adj = graph.adjacency_matrix();
        assert_relative_eq!(adj[(0, 1)], 1.0);
        assert_relative_eq!(adj[(1, 0)], 0.0);
    }

    #[test]
    fn test_laplacian() {
        let graph = KnowledgeGraphBuilder::new()
            .add_node("a", "A")
            .add_node("b", "B")
            .add_edge("a", "b", 1.0)
            .build();

        let lap = graph.laplacian_matrix();
        // L = [[1, -1], [-1, 1]] 对于无向图，这里是有向图
        assert_relative_eq!(lap[(0, 0)], 1.0);
        assert_relative_eq!(lap[(0, 1)], -1.0);
    }
}
