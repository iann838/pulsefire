import re


def transpile_typescript(source: str) -> str:
    out = source.split("TypedDict", 1)[1]
    out = re.sub(r"# (.+)\n", r"/* \1 */\n", out)
    out = re.sub(r"class (\w+):", r"}\n\nexport namespace \1 {", out)
    out = out.replace("\n\n}\n", "", 1) + "}\n"
    out = re.sub(r"(\w+) = TypedDict\(\"(\w+)\",", r"export interface \1", out)
    out = out.replace(", total=False)", "")
    out = out.replace("})", "}")
    out = re.sub(r"\bint\b", "number", out)
    out = re.sub(r"\bfloat\b", "number", out)
    out = re.sub(r"\bstr\b", "string", out)
    out = re.sub(r"\bbool\b", "boolean", out)
    out = re.sub(r"\bNone\b", "null", out)
    out = re.sub(r": \bNotRequired\[(.+)\]", r"?: \1", out)
    out = re.sub(r"\blist\[(.+)\]", r"\1[]", out)
    out = re.sub(r"\bdict\[(.+), (.+)\]", r"Record<\1, \2>", out)
    out = re.sub(r"\bdict\b", "Record<string, any>", out)
    out = re.sub(r"(\w+) = (\w+)", r"export interface \1 extends \2 {}", out)
    return out


with open("pulsefire/schemas.py") as source_f:
    with open("transpile/typescript/schemas.ts", "w+") as out_f:
        out_f.write(transpile_typescript(source_f.read()))
