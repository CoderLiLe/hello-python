"""学习路径索引 — 定义所有学习阶段及其文件列表"""
from typing import List, Dict, Optional

STAGES: List[Dict] = [
    {
        "id": "stage01_basic",
        "name": "Python基础",
        "description": "认识 Python：注释、print 输出、第一个程序",
        "requires": [],
        "files": ["comment.py", "print.py"],
    },
    {
        "id": "stage02_cycle",
        "name": "循环",
        "description": "while/for 循环、break/continue、循环嵌套",
        "requires": ["stage01_basic"],
        "files": [
            "cycle.py", "sum.py", "even_sum.py", "break.py", "continue.py",
            "print_star.py", "cycle_print_star.py", "print_end.py",
            "escape_character.py", "multiplication_table.py",
        ],
    },
    {
        "id": "stage03_function",
        "name": "函数",
        "description": "函数定义、参数、返回值、嵌套调用、模块化",
        "requires": ["stage02_cycle"],
        "files": [
            "first_func.py", "first_func_refact.py", "func_return_value.py",
            "function_parameters.py", "nested_func_calls.py",
            "print_line.py", "print_multiple_line.py", "multiplication_table.py",
            "import_func.py", "divider_module.py", "experience_module.py",
        ],
    },
    {
        "id": "stage04_advanced_grammar",
        "name": "高级语法",
        "description": "全局/局部变量、多返回值、默认参数、递归、拆包",
        "requires": ["stage03_function"],
        "files": [
            "global_variables.py", "global_variables2.py",
            "global_variable_name.py", "global_variables_location.py",
            "update_global_variables.py", "local_variables.py",
            "mult_return_values.py", "multi_parameters.py",
            "multi_parameter_sum.py", "default_func_parameters.py",
            "define_func_default_parameter.py", "notes_default_parameter.py",
            "parameter_passing.py", "func_modify_parameters.py",
            "recur_func_features.py", "recur_func_sum.py",
            "swap_nums.py", "unpack_tuple_dict.py", "plus_equal.py", "quote.py",
        ],
    },
    {
        "id": "stage05_advanced_data_structures",
        "name": "高级数据结构",
        "description": "列表、元组、字典、字符串的常用操作",
        "requires": ["stage02_cycle"],
        "files": [
            "list_basic_use.py", "list_traversal.py", "list_statistics.py",
            "list_sort.py", "tuple_basic_use.py", "tuple_traversal.py",
            "dictionary_definition.py", "dictionary_basic_use.py",
            "dictionary_other_use.py", "dictionary_traversal.py",
            "dictionary_application.py", "iterating_dict_list.py",
            "del_keyword.py", "string_definition_traversal.py",
            "string_judgment.py", "string_find_replace.py",
            "string_split_connect.py", "string_statistical.py",
            "string_alignment.py", "format_string.py",
        ],
    },
    {
        "id": "stage06_oop_basic",
        "name": "面向对象基础",
        "description": "类和对象、self、__init__、__str__、__del__",
        "requires": ["stage03_function"],
        "files": [
            "01_class_object.py", "02_self.py", "03_add_attributes.py",
            "04_init.py", "05_str_del.py", "06_sweet_potato.py", "07_furniture.py",
        ],
    },
    {
        "id": "stage07_oop_advanced",
        "name": "面向对象高级",
        "description": "多态、类属性、classmethod/staticmethod、__slots__",
        "requires": ["stage06_oop_basic"],
        "files": [
            "01_polymorphism.py", "02_class_attribute.py",
            "03_classmethod_static.py", "04_slots.py",
        ],
    },
    {
        "id": "stage08_oop_inherit",
        "name": "继承",
        "description": "单继承、多继承、重写、super()、私有属性",
        "requires": ["stage06_oop_basic"],
        "files": [
            "01_basic_inherit.py", "02_single_inherit.py",
            "03_multi_inherit.py", "04_override.py", "05_call_parent.py",
            "06_multi_level.py", "07_super.py", "08_private.py",
        ],
    },
    {
        "id": "stage09_oop_encapsulation",
        "name": "封装",
        "description": "属性封装、对象组合、综合练习",
        "requires": ["stage06_oop_basic"],
        "files": [
            "01_person_run.py", "02_house_furniture.py", "03_soldier_gun.py",
        ],
    },
    {
        "id": "stage10_oop_application",
        "name": "面向对象应用",
        "description": "扑克牌游戏、工资结算系统",
        "requires": ["stage08_oop_inherit", "stage09_oop_encapsulation"],
        "files": ["01_poker_game.py", "02_salary_system.py"],
    },
    {
        "id": "stage11_card_manage",
        "name": "综合应用 — 名片管理系统",
        "description": "名片管理 CRUD 系统，综合运用函数和数据结构",
        "requires": ["stage03_function", "stage05_advanced_data_structures"],
        "files": ["cards_main.py", "cards_tools.py"],
    },
]


def get_stage(stage_id: str) -> Optional[Dict]:
    """根据 id 获取学习阶段"""
    for stage in STAGES:
        if stage["id"] == stage_id:
            return stage
    return None


def list_stages() -> List[tuple]:
    """列出所有学习阶段，返回 [(id, name), ...]"""
    return [(s["id"], s["name"]) for s in STAGES]


def get_ordered_stages() -> List[Dict]:
    """按学习依赖关系排序的阶段列表（拓扑排序）"""
    ordered: List[Dict] = []
    remaining = list(STAGES)
    placed_ids: set = set()

    while remaining:
        ready = [
            s for s in remaining
            if all(r in placed_ids for r in s.get("requires", []))
        ]
        if not ready:
            # 循环依赖或无依赖可满足，按原顺序追加
            ordered.extend(remaining)
            break
        for stage in ready:
            ordered.append(stage)
            placed_ids.add(stage["id"])
            remaining.remove(stage)

    return ordered
