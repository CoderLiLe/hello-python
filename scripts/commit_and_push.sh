#!/bin/bash
# Git提交和推送脚本

set -euo pipefail

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 函数：打印带颜色的消息
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查是否在Git仓库中
check_git_repo() {
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        print_error "当前目录不是Git仓库"
        exit 1
    fi
}

# 检查是否有未提交的更改
check_uncommitted_changes() {
    if git diff-index --quiet HEAD --; then
        print_warning "没有未提交的更改"
        return 1
    fi
    return 0
}

# 运行代码检查
run_code_checks() {
    print_info "运行代码检查..."
    
    # 检查Python语法
    if command -v python3 &> /dev/null; then
        print_info "检查Python语法..."
        if ! python3 -m py_compile $(find . -name "*.py" -not -path "./.git/*" -not -path "./venv/*" -not -path "./__pycache__/*"); then
            print_error "Python语法检查失败"
            return 1
        fi
    fi
    
    # 运行测试
    if [ -f "Makefile" ]; then
        print_info "运行测试..."
        if ! make test; then
            print_error "测试失败"
            return 1
        fi
    fi
    
    print_success "代码检查通过"
    return 0
}

# 添加文件到Git
add_files() {
    local commit_type="$1"
    
    print_info "添加文件到Git..."
    
    case "$commit_type" in
        "all")
            git add .
            print_info "已添加所有文件"
            ;;
        "modified")
            git add -u
            print_info "已添加修改的文件"
            ;;
        "specific")
            print_info "请手动添加文件: git add <file1> <file2> ..."
            return 1
            ;;
        *)
            print_error "未知的提交类型: $commit_type"
            return 1
            ;;
    esac
    
    # 显示添加的文件
    print_info "已暂存的文件:"
    git diff --cached --name-only | while read -r file; do
        echo "  - $file"
    done
    
    return 0
}

# 创建提交信息
create_commit_message() {
    local commit_type="$1"
    local custom_message="$2"
    
    if [ -n "$custom_message" ]; then
        echo "$custom_message"
        return 0
    fi
    
    # 根据提交类型生成默认消息
    case "$commit_type" in
        "feat")
            echo "feat: 添加新功能"
            ;;
        "fix")
            echo "fix: 修复bug"
            ;;
        "docs")
            echo "docs: 更新文档"
            ;;
        "style")
            echo "style: 代码格式调整"
            ;;
        "refactor")
            echo "refactor: 代码重构"
            ;;
        "test")
            echo "test: 添加或更新测试"
            ;;
        "chore")
            echo "chore: 构建过程或辅助工具更新"
            ;;
        "optimize")
            echo "optimize: 项目优化和改进"
            ;;
        *)
            echo "chore: 常规更新"
            ;;
    esac
}

# 提交更改
commit_changes() {
    local commit_type="$1"
    local custom_message="$2"
    
    print_info "提交更改..."
    
    # 生成提交信息
    local commit_message
    commit_message=$(create_commit_message "$commit_type" "$custom_message")
    
    # 提交
    if git commit -m "$commit_message"; then
        print_success "提交成功: $commit_message"
        return 0
    else
        print_error "提交失败"
        return 1
    fi
}

# 推送到远程仓库
push_to_remote() {
    local branch="$1"
    local force="$2"
    
    print_info "推送到远程仓库..."
    
    # 获取远程仓库信息
    local remote
    remote=$(git remote)
    if [ -z "$remote" ]; then
        print_warning "没有配置远程仓库"
        return 0
    fi
    
    # 推送
    local push_cmd="git push"
    if [ "$force" = "true" ]; then
        push_cmd="$push_cmd --force"
        print_warning "使用强制推送"
    fi
    
    if $push_cmd origin "$branch"; then
        print_success "推送成功到 origin/$branch"
        return 0
    else
        print_error "推送失败"
        return 1
    fi
}

# 显示Git状态
show_git_status() {
    print_info "当前Git状态:"
    echo ""
    git status
    echo ""
    
    print_info "最近提交:"
    git log --oneline -5
    echo ""
}

# 显示帮助信息
show_help() {
    cat << EOF
Git提交和推送脚本

用法: $0 [选项]

选项:
  -t, --type TYPE     提交类型 (feat|fix|docs|style|refactor|test|chore|optimize)
  -m, --message MSG   自定义提交信息
  -a, --all           添加所有文件
  -u, --modified      只添加修改的文件
  -s, --specific      手动添加特定文件
  -c, --check         运行代码检查
  -p, --push          推送到远程仓库
  -f, --force         强制推送
  -b, --branch BRANCH 目标分支 (默认: 当前分支)
  -h, --help          显示帮助信息

示例:
  $0 -t feat -m "添加新功能" -a -p
  $0 -t fix -u -c
  $0 --type docs --message "更新文档" --all --push

提交类型说明:
  feat     新功能
  fix      bug修复
  docs     文档更新
  style    代码格式
  refactor 代码重构
  test     测试相关
  chore    构建过程
  optimize 优化改进
EOF
}

# 主函数
main() {
    # 默认值
    local commit_type="chore"
    local custom_message=""
    local add_type="modified"
    local run_checks=false
    local do_push=false
    local force_push=false
    local branch=""
    
    # 解析命令行参数
    while [[ $# -gt 0 ]]; do
        case $1 in
            -t|--type)
                commit_type="$2"
                shift 2
                ;;
            -m|--message)
                custom_message="$2"
                shift 2
                ;;
            -a|--all)
                add_type="all"
                shift
                ;;
            -u|--modified)
                add_type="modified"
                shift
                ;;
            -s|--specific)
                add_type="specific"
                shift
                ;;
            -c|--check)
                run_checks=true
                shift
                ;;
            -p|--push)
                do_push=true
                shift
                ;;
            -f|--force)
                force_push=true
                shift
                ;;
            -b|--branch)
                branch="$2"
                shift 2
                ;;
            -h|--help)
                show_help
                exit 0
                ;;
            *)
                print_error "未知选项: $1"
                show_help
                exit 1
                ;;
        esac
    done
    
    # 检查Git仓库
    check_git_repo
    
    # 显示当前状态
    show_git_status
    
    # 获取当前分支（如果未指定）
    if [ -z "$branch" ]; then
        branch=$(git branch --show-current)
        print_info "使用当前分支: $branch"
    fi
    
    # 检查是否有未提交的更改
    if ! check_uncommitted_changes; then
        print_warning "没有更改需要提交"
        exit 0
    fi
    
    # 运行代码检查
    if [ "$run_checks" = true ]; then
        if ! run_code_checks; then
            print_error "代码检查失败，请修复问题后再提交"
            exit 1
        fi
    fi
    
    # 添加文件
    if ! add_files "$add_type"; then
        print_error "添加文件失败"
        exit 1
    fi
    
    # 提交更改
    if ! commit_changes "$commit_type" "$custom_message"; then
        print_error "提交失败"
        exit 1
    fi
    
    # 推送到远程仓库
    if [ "$do_push" = true ]; then
        if ! push_to_remote "$branch" "$force_push"; then
            print_error "推送失败"
            exit 1
        fi
    fi
    
    print_success "✅ 所有操作完成！"
    
    # 显示最终状态
    show_git_status
}

# 运行主函数
main "$@"