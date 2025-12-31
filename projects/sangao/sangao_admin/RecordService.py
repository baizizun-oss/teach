# sangao_admin/RecordService.py

import re

def extract_teaching_chain(text: str):
    """
    从教学讲稿中提取递进式逻辑主线链条。
    支持两类典型范式：
      - 需求升级式（如网络：能用→方便→快→普适）
      - 概念建构式（如编程：问题→引入→澄清→辨析）
    返回一个字符串列表，每个元素是一个高层逻辑节点。
    """
    if not text or not text.strip():
        return ["输入文本为空"]

    text = re.sub(r'\s+', ' ', text).strip()
    sentences = re.split(r'(?<=[。？！；])', text)
    sentences = [s.strip() for s in sentences if s.strip()]

    # === 第一步：提取原始逻辑节点（细粒度）===
    chain = []
    current_problem = None

    for sent in sentences:
        # ====== 通用问题检测 ======
        is_problem = False
        problem_type = None

        # 网络类问题
        if "为什么" in sent:
            if "IP" in sent:
                problem_type = "需要网络地址"
                is_problem = True
            elif "DNS" in sent or ("查IP" in sent or "通讯录" in sent):
                problem_type = "手动查IP太麻烦"
                is_problem = True
            elif "更快" in sent or "网速" in sent or "带宽" in sent:
                problem_type = "想让网络更快"
                is_problem = True
            elif "搬家" in sent or "复用" in sent or "路由器" in sent and "不能用" in sent:
                problem_type = "设备无法跨地复用"
                is_problem = True
        elif "缺点" in sent and ("无地址" in sent or "谁都能够接受" in sent):
            problem_type = "无地址网络不安全"
            is_problem = True
        elif "需求" in sent:
            if "更快" in sent:
                problem_type = "追求更高网速"
            else:
                problem_type = "需要更普适的网络使用方式"
            is_problem = True

        # 编程类问题
        elif ("变量" in sent and ("太多" in sent or "繁琐" in sent or "很多个" in sent)) or \
             ("有没有.*更好.*方法" in sent.replace(" ", "")):
            problem_type = "手动变量排序繁琐"
            is_problem = True
        elif "sort" in sent and ("none" in sent.lower() or "返回值" in sent or "输出nine" in sent or "原地" in sent):
            problem_type = "误解 sort() 返回新列表"
            is_problem = True
        elif "字典" in sent and ("写法" in sent or "error" in sent or "键值" in sent or "混淆" in sent):
            problem_type = "混淆列表与字典语法"
            is_problem = True
        elif any(re.search(p, sent) for p in [
            r'是不是.*麻烦', r'能不能.*更简单', r'这样.*对吗', r'发现.*error'
        ]):
            problem_type = "存在效率或认知障碍"
            is_problem = True

        if is_problem:
            current_problem = problem_type
            continue

        # ====== 解决方案 / 教学动作检测 ======
        added = False

        # 网络类解决方案
        if "这就是" in sent and ("IP" in sent or "地址" in sent):
            sol = "有地址的网络，也就是IP地址"
            if current_problem:
                chain.append(f"{current_problem} → {sol}")
                current_problem = None
            else:
                chain.append(sol)
            added = True
        elif "DNS" in sent and ("服务器" in sent or "自动" in sent):
            sol = "DNS自动解析"
            if current_problem:
                chain.append(f"{current_problem} → {sol}")
                current_problem = None
            else:
                chain.append(sol)
            added = True
        elif "网速" in sent and "比特" in sent:
            chain.append("网速用每秒传输的比特数衡量")
            added = True
        elif "带宽" in sent and ("水管" in sent or "最大速度" in sent):
            chain.append("带宽是网络的最大传输速率")
            added = True
        elif "路由器" in sent and ("配置" in sent or "复用" in sent):
            chain.append("通过软件配置实现路由器多地复用")
            added = True

        # 编程类解决方案
        elif "列表" in sent and ("这一节要学" in sent or "更简单的方法" in sent or "中括号" in sent):
            sol = "引入列表简化操作"
            if current_problem:
                chain.append(f"{current_problem} → {sol}")
                current_problem = None
            else:
                chain.append(sol)
            added = True
        elif "sort" in sent and ("原地排序" in sent or "返回值是none" in sent or "先排序再输出" in sent):
            chain.append("澄清 sort() 原地修改的特性")
            added = True
        elif ("列表" in sent or "字典" in sent) and ("区分" in sent or "不要混淆" in sent or "键值对" in sent):
            chain.append("区分列表与字典的语法差异")
            added = True

        # 通用解决方案句式
        if not added:
            for pattern in [r'这就是(.+?)[。！]', r'所以(.+?)[。！]', r'对，(.+?)[。！]']:
                m = re.search(pattern, sent)
                if m:
                    sol_text = m.group(1).strip()
                    # 简单过滤太具体的描述
                    if len(sol_text) < 20 and not any(k in sol_text for k in ["填进去", "报错了", "打开"]):
                        if current_problem:
                            chain.append(f"{current_problem} → {sol_text}")
                            current_problem = None
                        else:
                            chain.append(sol_text)
                        added = True
                        break

    # === 第二步：映射为高层教学逻辑链（去重 + 抽象）===
    high_level_chain = []
    seen = set()

    for item in chain:
        # 网络类高层节点
        if "安全" in item or "无地址" in item:
            key = "网络如何安全运行"
        elif "IP" in item and ("地址" in item or "网络地址" in item):
            key = "有地址的网络，也就是IP地址"
        elif "麻烦" in item or "查IP" in item:
            key = "能运行了但太麻烦"
        elif "DNS" in item:
            key = "DNS自动解析"
        elif "更快" in item or "网速" in item:
            key = "方便了之后还想让他更快"
        elif "带宽" in item:
            key = "理解带宽限制"
        elif "路由器" in item and ("复用" in item or "配置" in item):
            key = "最后还想让他更普适"

        # 编程类高层节点
        elif "手动变量" in item or "繁琐" in item:
            key = "手动变量排序繁琐"
        elif "引入列表" in item:
            key = "引入列表简化操作"
        elif "sort" in item and "原地" in item:
            key = "澄清 sort() 原地修改的特性"
        elif "区分" in item and ("列表" in item or "字典" in item):
            key = "区分列表与字典的语法差异"

        else:
            # 保留其他有效节点（如通用解法）
            key = item

        if key and key not in seen:
            high_level_chain.append(key)
            seen.add(key)

    if not high_level_chain:
        return ["未能提取有效教学逻辑链"]

    # 如果全是低层细节，回退到前3个
    if len(high_level_chain) == 1 and len(chain) > 1:
        return chain[:3]

    return high_level_chain


def infer_teaching_pattern(chain: list) -> str:
    """根据逻辑链推断教学范式"""
    all_text = "".join(chain)
    if any(kw in all_text for kw in ["安全", "方便", "更快", "普适", "复用", "带宽", "需求升级"]):
        return "需求升级式（层层递进）"
    elif any(kw in all_text for kw in ["澄清", "区分", "误解", "注意", "弄清楚", "混淆", "繁琐", "引入列表"]):
        return "概念建构式（聚焦澄清）"
    else:
        return "未识别范式"