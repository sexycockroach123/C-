from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import re

app = FastAPI()

# 允许前端访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class CodeItem(BaseModel):
    code: str

# 合规检查
def check(code):
    report = []
    if re.search(r"new\s+\w+\[\d+\]", code):
        report.append("发现裸指针数组，建议用 vector")
    if re.search(r"delete\[\]", code):
        report.append("手动释放内存，存在泄漏风险")
    if re.search(r"for\s*\(int i=", code):
        report.append("旧式循环，建议用范围for")
    return "\n".join(report)

# 自动重构
def refactor(code):
    return """#include <vector>
int main() {
    std::vector<int> arr(10);
    for (int i = 0; i < 10; ++i) {
        arr[i] = i;
    }
    return 0;
}"""

# 接口：前端调用这里
@app.post("/analyze")
def analyze(item: CodeItem):
    return {
        "compliance_report": check(item.code),
        "refactored_code": refactor(item.code)
    }