//! # 算子系统运行时
//!
//! 提供Web API服务，支持算子编排、执行、知识图谱查询等

use axum::{
    extract::State,
    http::StatusCode,
    response::Json,
    routing::{get, post},
    Router,
};
use operator_core::category::Workflow;
use operator_core::operator::{FunctionOperator, IdentityOperator, LinearOperator, Operator};
use operator_core::state::StateVector;
use operator_core::{ExecutionContext, ExecutionResult};
use operator_graph::{KnowledgeGraph, KnowledgeGraphBuilder, KnowledgeNode, KnowledgeEdge};
use operator_wasm::WasmPluginManager;
use serde::{Deserialize, Serialize};
use std::sync::Arc;
use tokio::sync::Mutex;
use tower_http::cors::CorsLayer;
use tower_http::services::ServeDir;

/// 应用状态
struct AppState {
    operators: Mutex<Vec<OperatorInfo>>,
    knowledge_graph: Mutex<KnowledgeGraph>,
    plugin_manager: Mutex<WasmPluginManager>,
    execution_logs: Mutex<Vec<ExecutionLog>>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
struct OperatorInfo {
    id: String,
    name: String,
    description: String,
    input_type: String,
    output_type: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
struct ExecutionLog {
    timestamp: u64,
    operator_id: String,
    success: bool,
    execution_time_ms: u64,
    residual: f64,
}

#[derive(Debug, Deserialize)]
struct ExecuteRequest {
    workflow: Vec<String>,
    input: Vec<f64>,
}

#[derive(Debug, Serialize)]
struct ExecuteResponse {
    success: bool,
    output: Option<Vec<f64>>,
    execution_time_ms: u64,
    logs: Vec<String>,
    error: Option<String>,
}

#[derive(Debug, Deserialize)]
struct AddNodeRequest {
    id: String,
    label: String,
}

#[derive(Debug, Deserialize)]
struct AddEdgeRequest {
    source: String,
    target: String,
    weight: f64,
}

#[derive(Debug, Serialize)]
struct GraphData {
    nodes: Vec<NodeData>,
    edges: Vec<EdgeData>,
}

#[derive(Debug, Serialize)]
struct NodeData {
    id: String,
    label: String,
    pagerank: f64,
}

#[derive(Debug, Serialize)]
struct EdgeData {
    source: String,
    target: String,
    weight: f64,
}

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    operator_core::init_logging();
    tracing::info!("启动算子统一系统服务器...");

    // 初始化状态
    let mut plugin_manager = WasmPluginManager::new("./plugins");
    plugin_manager.load_all()?;

    // 初始化知识图谱示例数据
    let mut kg = KnowledgeGraphBuilder::new()
        .add_node("op1", "代码编译算子")
        .add_node("op2", "全文搜索算子")
        .add_node("op3", "图片处理算子")
        .add_node("op4", "需求分析算子")
        .add_node("op5", "知识图谱算子")
        .add_edge("op4", "op1", 0.8)
        .add_edge("op4", "op2", 0.9)
        .add_edge("op4", "op5", 0.95)
        .add_edge("op1", "op3", 0.7)
        .add_edge("op2", "op5", 0.6)
        .build();

    let state = Arc::new(AppState {
        operators: Mutex::new(vec![
            OperatorInfo {
                id: "identity".to_string(),
                name: "恒等算子".to_string(),
                description: "输出等于输入".to_string(),
                input_type: "StateVector".to_string(),
                output_type: "StateVector".to_string(),
            },
            OperatorInfo {
                id: "linear".to_string(),
                name: "线性变换算子".to_string(),
                description: "y = 2x".to_string(),
                input_type: "StateVector".to_string(),
                output_type: "StateVector".to_string(),
            },
            OperatorInfo {
                id: "normalize".to_string(),
                name: "归一化算子".to_string(),
                description: "归一化到单位范数".to_string(),
                input_type: "StateVector".to_string(),
                output_type: "StateVector".to_string(),
            },
            OperatorInfo {
                id: "relu".to_string(),
                name: "ReLU激活算子".to_string(),
                description: "max(0, x)".to_string(),
                input_type: "StateVector".to_string(),
                output_type: "StateVector".to_string(),
            },
        ]),
        knowledge_graph: Mutex::new(kg),
        plugin_manager: Mutex::new(plugin_manager),
        execution_logs: Mutex::new(Vec::new()),
    });

    // 创建路由
    let app = Router::new()
        .route("/api/health", get(health))
        .route("/api/operators", get(list_operators))
        .route("/api/execute", post(execute_workflow))
        .route("/api/graph", get(get_graph))
        .route("/api/graph/node", post(add_node))
        .route("/api/graph/edge", post(add_edge))
        .route("/api/plugins", get(list_plugins))
        .route("/api/logs", get(get_logs))
        .route("/api/status", get(get_status))
        .nest_service("/", ServeDir::new("./frontend/dist"))
        .layer(CorsLayer::permissive())
        .with_state(state);

    let addr = "0.0.0.0:3000";
    tracing::info!("服务器监听在 http://{}", addr);
    println!("🚀 算子统一系统已启动: http://localhost:3000");
    axum::Server::bind(&addr.parse().unwrap())
        .serve(app.into_make_service())
        .await?;

    Ok(())
}

async fn health() -> &'static str {
    "OK"
}

async fn list_operators(State(state): State<Arc<AppState>>) -> Json<Vec<OperatorInfo>> {
    let ops = state.operators.lock().await;
    Json(ops.clone())
}

async fn execute_workflow(
    State(state): State<Arc<AppState>>,
    Json(req): Json<ExecuteRequest>,
) -> Json<ExecuteResponse> {
    let start = std::time::Instant::now();
    let mut ctx = ExecutionContext::default();
    let input = StateVector::from_vec(req.input);

    // 构建工作流
    let mut workflow = Workflow::new("user-workflow");
    for op_id in req.workflow {
        match op_id.as_str() {
            "identity" => {
                let op = IdentityOperator::new(input.dimension);
                workflow = match workflow.then(op) {
                    Ok(w) => w,
                    Err(e) => {
                        return Json(ExecuteResponse {
                            success: false,
                            output: None,
                            execution_time_ms: start.elapsed().as_millis() as u64,
                            logs: vec![],
                            error: Some(e.to_string()),
                        });
                    }
                };
            }
            "linear" => {
                let n = input.dimension;
                let matrix = nalgebra::DMatrix::from_diagonal_element(n, n, 2.0);
                let op = LinearOperator::new(matrix);
                workflow = match workflow.then(op) {
                    Ok(w) => w,
                    Err(e) => {
                        return Json(ExecuteResponse {
                            success: false,
                            output: None,
                            execution_time_ms: start.elapsed().as_millis() as u64,
                            logs: vec![],
                            error: Some(e.to_string()),
                        });
                    }
                };
            }
            "normalize" => {
                let op = FunctionOperator::new("normalize", |s: &StateVector, _ctx| {
                    let mut s = s.clone();
                    s.normalize();
                    Ok(s)
                });
                workflow = match workflow.then(op) {
                    Ok(w) => w,
                    Err(e) => {
                        return Json(ExecuteResponse {
                            success: false,
                            output: None,
                            execution_time_ms: start.elapsed().as_millis() as u64,
                            logs: vec![],
                            error: Some(e.to_string()),
                        });
                    }
                };
            }
            "relu" => {
                let op = FunctionOperator::new("relu", |s: &StateVector, _ctx| {
                    let mut result = s.clone();
                    for i in 0..result.dimension {
                        result[i] = result[i].max(0.0);
                    }
                    Ok(result)
                });
                workflow = match workflow.then(op) {
                    Ok(w) => w,
                    Err(e) => {
                        return Json(ExecuteResponse {
                            success: false,
                            output: None,
                            execution_time_ms: start.elapsed().as_millis() as u64,
                            logs: vec![],
                            error: Some(e.to_string()),
                        });
                    }
                };
            }
            _ => {
                return Json(ExecuteResponse {
                    success: false,
                    output: None,
                    execution_time_ms: start.elapsed().as_millis() as u64,
                    logs: vec![],
                    error: Some(format!("未知算子: {}", op_id)),
                });
            }
        }
    }

    // 执行工作流
    match workflow.execute(&input, &mut ctx) {
        Ok(result) => {
            // 记录日志
            let mut logs = state.execution_logs.lock().await;
            logs.push(ExecutionLog {
                timestamp: std::time::SystemTime::now()
                    .duration_since(std::time::UNIX_EPOCH)
                    .unwrap()
                    .as_millis() as u64,
                operator_id: "workflow".to_string(),
                success: result.success,
                execution_time_ms: result.execution_time_ms,
                residual: result.residual,
            });

            Json(ExecuteResponse {
                success: result.success,
                output: result.output_state.map(|s| s.to_vec()),
                execution_time_ms: result.execution_time_ms,
                logs: result.logs,
                error: result.error,
            })
        }
        Err(e) => Json(ExecuteResponse {
            success: false,
            output: None,
            execution_time_ms: start.elapsed().as_millis() as u64,
            logs: vec![],
            error: Some(e.to_string()),
        }),
    }
}

async fn get_graph(State(state): State<Arc<AppState>>) -> Json<GraphData> {
    let kg = state.knowledge_graph.lock().await;
    let pagerank = kg.pagerank(20);

    let nodes = kg
        .nodes()
        .iter()
        .map(|n| NodeData {
            id: n.id.clone(),
            label: n.label.clone(),
            pagerank: *pagerank.get(&n.id).unwrap_or(&0.0),
        })
        .collect();

    let edges = kg
        .edges()
        .iter()
        .map(|e| EdgeData {
            source: e.source.clone(),
            target: e.target.clone(),
            weight: e.weight,
        })
        .collect();

    Json(GraphData { nodes, edges })
}

async fn add_node(
    State(state): State<Arc<AppState>>,
    Json(req): Json<AddNodeRequest>,
) -> StatusCode {
    let mut kg = state.knowledge_graph.lock().await;
    kg.add_node(KnowledgeNode {
        id: req.id,
        label: req.label,
        properties: serde_json::json!({}),
        embedding: None,
    });
    StatusCode::OK
}

async fn add_edge(
    State(state): State<Arc<AppState>>,
    Json(req): Json<AddEdgeRequest>,
) -> StatusCode {
    let mut kg = state.knowledge_graph.lock().await;
    let _ = kg.add_edge(KnowledgeEdge {
        source: req.source,
        target: req.target,
        weight: req.weight,
        relation_type: "related".to_string(),
        properties: serde_json::json!({}),
    });
    StatusCode::OK
}

async fn list_plugins(State(state): State<Arc<AppState>>) -> Json<Vec<String>> {
    let pm = state.plugin_manager.lock().await;
    Json(pm.list())
}

async fn get_logs(State(state): State<Arc<AppState>>) -> Json<Vec<ExecutionLog>> {
    let logs = state.execution_logs.lock().await;
    Json(logs.clone())
}

async fn get_status(State(state): State<Arc<AppState>>) -> Json<serde_json::Value> {
    let kg = state.knowledge_graph.lock().await;
    let pm = state.plugin_manager.lock().await;
    let ops = state.operators.lock().await;
    let logs = state.execution_logs.lock().await;

    Json(serde_json::json!({
        "operators_count": ops.len(),
        "plugins_count": pm.list().len(),
        "graph_nodes": kg.node_count(),
        "graph_edges": kg.edge_count(),
        "executions_count": logs.len(),
        "success_rate": if logs.is_empty() { 100.0 } else {
            logs.iter().filter(|l| l.success).count() as f64 / logs.len() as f64 * 100.0
        },
        "status": "running"
    }))
}
