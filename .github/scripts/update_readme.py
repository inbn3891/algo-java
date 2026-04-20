import os
import re
import subprocess

PLATFORM_MAP = {"PGS": "프로그래머스"}

FOLDER_MAP = {
    "dfs-bfs": "DFS/BFS", "dp": "DP", "greedy": "Greedy",
    "graph": "Graph", "tree": "Tree", "sort": "Sort",
    "binary-search": "Binary Search", "stack-queue": "Stack/Queue",
    "hash": "Hash", "string": "String"
}

result = subprocess.check_output(
    ["git", "diff", "--name-only", "--diff-filter=A", "HEAD~1", "HEAD"],
    env={**os.environ, "GIT_TERMINAL_PROMPT": "0", "LANG": "ko_KR.UTF-8"}
)
new_files = result.decode("utf-8").strip().splitlines()
new_files = [f for f in new_files if f.endswith(".java")]

# 한글 이스케이프 처리
decoded_files = []
for f in new_files:
    if f.startswith('"') and f.endswith('"'):
        f = f[1:-1].encode('raw_unicode_escape').decode('unicode_escape').encode('latin-1').decode('utf-8')
    decoded_files.append(f)
new_files = decoded_files

if not new_files:
    print("새로 추가된 java 파일 없음")
    exit(0)

with open("README.md", "r", encoding="utf-8") as f:
    content = f.read()

for file in new_files:
    parts = os.path.basename(file).replace(".java", "").split("_", 2)
    if len(parts) < 3:
        continue
    platform_code, level, problem = parts
    platform = PLATFORM_MAP.get(platform_code, platform_code)
    folder = file.split("/")[0]
    section = FOLDER_MAP.get(folder)
    if not section:
        continue

    new_row = f"| {problem} | {platform} | {level} | [풀이](./{file}) |"
    section_header = f"## {section}"
    lines = content.splitlines()
    new_lines = []
    in_section = False
    inserted = False

    for i, line in enumerate(lines):
        new_lines.append(line)
        if line.strip() == section_header:
            in_section = True
        elif in_section and not inserted:
            if line.startswith("## ") and line.strip() != section_header:
                new_lines.insert(-1, new_row)
                inserted = True
                in_section = False
            elif i == len(lines) - 1:
                new_lines.append(new_row)
                inserted = True

    if inserted:
        content = "\n".join(new_lines) + "\n"

for folder, section in FOLDER_MAP.items():
    count = len([f for f in os.listdir(folder) if f.endswith(".java")]) if os.path.exists(folder) else 0
    content = re.sub(
        rf"\| {re.escape(section)} \| .* \|",
        f"| {section} | {count} |",
        content
    )

with open("README.md", "w", encoding="utf-8") as f:
    f.write(content)

print("README 업데이트 완료")