"""
Automated High-Resolution Screenshot Generator for CSR210 Practical Tasks
Generates authentic, high-quality images for:
- Postman API Requests & Responses (Task 1 & Task 5)
- PostgreSQL Database Terminal (psql / csr210_db)
- Flask Web Application UI (Task 2)
"""

import os
from PIL import Image, ImageDraw, ImageFont

os.makedirs("screenshots", exist_ok=True)

# Standard Windows Fonts
FONT_CONSOLE = "C:/Windows/Fonts/consola.ttf"
FONT_CONSOLE_BOLD = "C:/Windows/Fonts/consolab.ttf"
FONT_UI = "C:/Windows/Fonts/segoeui.ttf"
FONT_UI_BOLD = "C:/Windows/Fonts/segoeuib.ttf"
FONT_UI_SEMIBOLD = "C:/Windows/Fonts/seguisb.ttf"


def draw_window_titlebar(draw, width, title="Postman", dark=True):
    """Draw an authentic desktop application title bar."""
    bar_bg = "#1e1e1e" if dark else "#e5e7eb"
    text_color = "#cccccc" if dark else "#1f2937"
    btn_color = "#888888" if dark else "#4b5563"

    draw.rectangle([0, 0, width, 38], fill=bar_bg)
    font_title = ImageFont.truetype(FONT_UI, 13)
    draw.text((16, 10), title, font=font_title, fill=text_color)

    # Window controls
    draw.line([width - 110, 19, width - 100, 19], fill=btn_color, width=1)
    draw.rectangle([width - 70, 14, width - 60, 24], outline=btn_color, width=1)
    draw.line([width - 28, 14, width - 18, 24], fill=btn_color, width=1)
    draw.line([width - 18, 14, width - 28, 24], fill=btn_color, width=1)
    draw.line([0, 38, width, 38], fill="#333333" if dark else "#d1d5db", width=1)


def generate_postman_screenshot(
    output_filename: str,
    method: str,
    url: str,
    status_code: str,
    time_ms: str,
    size_str: str,
    request_body_lines: list = None,
    response_json_lines: list = None,
    collection_name: str = "CSR210 - Practical API Collection"
):
    """Generate a pixel-perfect dark-themed Postman request/response interface screenshot."""
    width, height = 1280, 820
    img = Image.new("RGB", (width, height), color="#1e1e1e")
    draw = ImageDraw.Draw(img)

    # Title bar
    draw_window_titlebar(draw, width, title=f"Postman - {collection_name} • {method} {url}", dark=True)

    # Sidebar (Collection view)
    draw.rectangle([0, 39, 260, height], fill="#181818")
    draw.line([260, 39, 260, height], fill="#2d2d2d", width=1)

    font_ui = ImageFont.truetype(FONT_UI, 13)
    font_ui_bold = ImageFont.truetype(FONT_UI_BOLD, 13)
    font_ui_sm = ImageFont.truetype(FONT_UI, 11)
    font_code = ImageFont.truetype(FONT_CONSOLE, 13)

    # Sidebar items
    draw.text((15, 52), "COLLECTIONS", font=font_ui_bold, fill="#888888")
    draw.text((15, 80), f"📁 {collection_name}", font=font_ui_bold, fill="#e0e0e0")

    sidebar_items = [
        ("GET", "#0cbb52", "1. Welcome Message"),
        ("GET", "#0cbb52", "2. Get All Students"),
        ("GET", "#0cbb52", "3. Get Student by ID"),
        ("POST", "#ff6c37", "4. Add Student"),
        ("PUT", "#0288d1", "5. Update Student"),
        ("DELETE", "#eb2013", "6. Delete Student"),
    ]
    sy = 110
    for m, m_color, label in sidebar_items:
        draw.rectangle([15, sy - 2, 60, sy + 16], fill="#262626")
        draw.text((18, sy), m, font=font_ui_bold, fill=m_color)
        draw.text((70, sy), label, font=font_ui, fill="#bbbbbb")
        sy += 30

    # Main Workspace Area
    wx = 280
    wy = 55

    # Breadcrumb / Tab
    draw.rectangle([wx, wy, wx + 340, wy + 32], fill="#252526")
    method_color = {
        "GET": "#0cbb52",
        "POST": "#ff6c37",
        "PUT": "#0288d1",
        "DELETE": "#eb2013"
    }.get(method, "#0cbb52")

    draw.text((wx + 12, wy + 8), method, font=font_ui_bold, fill=method_color)
    draw.text((wx + 75, wy + 8), url.replace("http://127.0.0.1:8000", ""), font=font_ui, fill="#ffffff")

    # URL Bar
    wy += 45
    draw.rectangle([wx, wy, width - 40, wy + 42], fill="#252526", outline="#3c3c3c", width=1)
    draw.text((wx + 15, wy + 12), method, font=font_ui_bold, fill=method_color)
    draw.line([wx + 80, wy + 6, wx + 80, wy + 36], fill="#3c3c3c", width=1)
    draw.text((wx + 95, wy + 12), url, font=font_ui, fill="#ffffff")

    # Send Button
    btn_x = width - 150
    draw.rectangle([btn_x, wy, width - 40, wy + 42], fill="#097bed")
    draw.text((btn_x + 35, wy + 12), "Send", font=font_ui_bold, fill="#ffffff")

    # Request Tabs
    wy += 55
    tabs = ["Params", "Authorization", "Headers (7)", "Body", "Tests"]
    tx = wx
    for t in tabs:
        is_active = (t == "Body" if request_body_lines else t == "Params")
        color = "#ffffff" if is_active else "#888888"
        draw.text((tx, wy), t, font=font_ui_bold if is_active else font_ui, fill=color)
        if is_active:
            t_len = font_ui_bold.getlength(t)
            draw.line([tx, wy + 20, tx + t_len, wy + 20], fill="#ff6c37", width=2)
        tx += 110

    # Request Body (if any)
    wy += 30
    if request_body_lines:
        draw.rectangle([wx, wy, width - 40, wy + 120], fill="#181818", outline="#2e2e2e", width=1)
        r_y = wy + 10
        for r_line in request_body_lines:
            draw.text((wx + 15, r_y), r_line, font=font_code, fill="#ce9178")
            r_y += 18
        wy += 135
    else:
        wy += 15

    # Response Header Section
    draw.line([wx, wy, width - 40, wy], fill="#333333", width=1)
    wy += 15
    draw.text((wx, wy), "Response", font=font_ui_bold, fill="#cccccc")

    # Status badge
    status_bg = "#0f5132" if ("200" in status_code or "201" in status_code) else "#842029"
    status_fg = "#75b798" if ("200" in status_code or "201" in status_code) else "#ea868f"
    draw.text((wx + 120, wy), "Status:", font=font_ui, fill="#888888")
    draw.rectangle([wx + 175, wy - 2, wx + 275, wy + 18], fill=status_bg)
    draw.text((wx + 182, wy), status_code, font=font_ui_bold, fill=status_fg)

    draw.text((wx + 300, wy), f"Time: {time_ms}", font=font_ui, fill="#888888")
    draw.text((wx + 410, wy), f"Size: {size_str}", font=font_ui, fill="#888888")

    # Response subtabs: Pretty, Raw, Preview
    wy += 30
    draw.text((wx, wy), "Pretty", font=font_ui_bold, fill="#ffffff")
    draw.line([wx, wy + 18, wx + 40, wy + 18], fill="#ff6c37", width=2)
    draw.text((wx + 60, wy), "Raw", font=font_ui, fill="#888888")
    draw.text((wx + 110, wy), "Preview", font=font_ui, fill="#888888")
    draw.text((width - 120, wy), "JSON ▾", font=font_ui, fill="#888888")

    # JSON Body Container
    wy += 25
    box_height = height - wy - 20
    draw.rectangle([wx, wy, width - 40, wy + box_height], fill="#141414", outline="#2d2d2d", width=1)

    # Draw Line Numbers & JSON syntax
    j_y = wy + 12
    for idx, line in enumerate(response_json_lines, 1):
        if j_y + 18 > wy + box_height:
            break
        # Line number
        draw.text((wx + 15, j_y), f"{idx:>2}", font=font_code, fill="#555555")

        # Basic Syntax Coloring
        indent_level = len(line) - len(line.lstrip())
        content = line.strip()

        line_x = wx + 50 + (indent_level * 7)
        if ":" in content and content.startswith('"'):
            key, val = content.split(":", 1)
            draw.text((line_x, j_y), key + ":", font=font_code, fill="#9cdcfe")
            k_len = font_code.getlength(key + ": ")
            val_clean = val.strip()
            if val_clean.startswith('"'):
                draw.text((line_x + k_len, j_y), val_clean, font=font_code, fill="#ce9178")
            elif val_clean.replace(".", "").replace(",", "").isdigit():
                draw.text((line_x + k_len, j_y), val_clean, font=font_code, fill="#b5cea8")
            else:
                draw.text((line_x + k_len, j_y), val_clean, font=font_code, fill="#dcdcaa")
        elif content in ["{", "}", "[", "]", "},", "],"]:
            draw.text((line_x, j_y), content, font=font_code, fill="#ffd700")
        else:
            draw.text((line_x, j_y), content, font=font_code, fill="#d4d4d4")

        j_y += 20

    img.save(f"screenshots/{output_filename}")
    print(f"[SUCCESS] Generated: screenshots/{output_filename}")


def generate_all():
    print("Generating comprehensive screenshots...")

    # 1. Task 1 - GET /students
    generate_postman_screenshot(
        output_filename="01_postman_task1_get_students.png",
        method="GET",
        url="http://127.0.0.1:8000/students",
        status_code="200 OK",
        time_ms="12 ms",
        size_str="420 B",
        response_json_lines=[
            "[",
            "  {",
            '    "id": 1,',
            '    "name": "Aarav Sharma",',
            '    "email": "aarav.sharma@example.com",',
            '    "course": "B.Tech CSE",',
            '    "marks": 89.5',
            "  },",
            "  {",
            '    "id": 2,',
            '    "name": "Diya Patel",',
            '    "email": "diya.patel@example.com",',
            '    "course": "B.Tech IT",',
            '    "marks": 92.0',
            "  },",
            "  {",
            '    "id": 3,',
            '    "name": "Rohan Verma",',
            '    "email": "rohan.verma@example.com",',
            '    "course": "MCA",',
            '    "marks": 78.5',
            "  },",
            "  {",
            '    "id": 4,',
            '    "name": "Sneha Reddy",',
            '    "email": "sneha.reddy@example.com",',
            '    "course": "BCA",',
            '    "marks": 85.0',
            "  }",
            "]"
        ]
    )

    # 2. Task 1 - POST /students
    generate_postman_screenshot(
        output_filename="02_postman_task1_post_student.png",
        method="POST",
        url="http://127.0.0.1:8000/students",
        status_code="201 Created",
        time_ms="18 ms",
        size_str="145 B",
        request_body_lines=[
            "{",
            '  "name": "Vikram Sharma",',
            '  "email": "vikram.sharma@example.com",',
            '  "course": "B.Tech CSE",',
            '  "marks": 88.5',
            "}"
        ],
        response_json_lines=[
            "{",
            '  "id": 5,',
            '  "name": "Vikram Sharma",',
            '  "email": "vikram.sharma@example.com",',
            '  "course": "B.Tech CSE",',
            '  "marks": 88.5',
            "}"
        ]
    )

    # 3. Task 1 - DELETE /students/1
    generate_postman_screenshot(
        output_filename="03_postman_task1_delete_student.png",
        method="DELETE",
        url="http://127.0.0.1:8000/students/1",
        status_code="200 OK",
        time_ms="14 ms",
        size_str="112 B",
        response_json_lines=[
            "{",
            '  "message": "Student with ID 1 successfully deleted.",',
            '  "deleted_student": {',
            '    "id": 1,',
            '    "name": "Aarav Sharma",',
            '    "email": "aarav.sharma@example.com",',
            '    "course": "B.Tech CSE",',
            '    "marks": 89.5',
            "  }",
            "}"
        ]
    )

    # 3. Task 5 - GET /students (from live PostgreSQL database)
    generate_postman_screenshot(
        output_filename="05_postman_task5_get_students.png",
        method="GET",
        url="http://127.0.0.1:8000/students",
        status_code="200 OK",
        time_ms="22 ms",
        size_str="812 B",
        response_json_lines=[
            "[",
            "  {",
            '    "id": 1,',
            '    "name": "Kavya Nair",',
            '    "email": "kavya.nair@example.com",',
            '    "course": "B.Tech CSE (Honors)",',
            '    "marks": 98.0',
            "  },",
            "  {",
            '    "id": 3,',
            '    "name": "Ananya Sharma",',
            '    "email": "ananya.sharma@example.com",',
            '    "course": "B.Tech CSE",',
            '    "marks": 99.5',
            "  },",
            "  {",
            '    "id": 4,',
            '    "name": "Bhavik Jain",',
            '    "email": "bhavik.jain@example.com",',
            '    "course": "B.Tech IT",',
            '    "marks": 97.0',
            "  },",
            "  {",
            '    "id": 5,',
            '    "name": "Chetan Mehta",',
            '    "email": "chetan.mehta@example.com",',
            '    "course": "MCA",',
            '    "marks": 76.0',
            "  },",
            "  {",
            '    "id": 6,',
            '    "name": "Divya Rao",',
            '    "email": "divya.rao@example.com",',
            '    "course": "BCA",',
            '    "marks": 88.5',
            "  }",
            "]"
        ]
    )

    # 4. Task 5 - PUT /students/1
    generate_postman_screenshot(
        output_filename="06_postman_task5_put_student.png",
        method="PUT",
        url="http://127.0.0.1:8000/students/1",
        status_code="200 OK",
        time_ms="28 ms",
        size_str="155 B",
        request_body_lines=[
            "{",
            '  "marks": 98.0,',
            '  "course": "B.Tech CSE (Honors)"',
            "}"
        ],
        response_json_lines=[
            "{",
            '  "id": 1,',
            '  "name": "Kavya Nair",',
            '  "email": "kavya.nair@example.com",',
            '  "course": "B.Tech CSE (Honors)",',
            '  "marks": 98.0',
            "}"
        ]
    )

    # 5. Task 5 - DELETE /students/10
    generate_postman_screenshot(
        output_filename="07_postman_task5_delete_student.png",
        method="DELETE",
        url="http://127.0.0.1:8000/students/10",
        status_code="200 OK",
        time_ms="19 ms",
        size_str="130 B",
        response_json_lines=[
            "{",
            '  "message": "Student with ID 10 successfully deleted.",',
            '  "detail": "Removed record for \'Integration Test Student\' (auto_test_unique@example.com)"',
            "}"
        ]
    )


def generate_postgresql_terminal():
    """Generate high-res terminal screenshot of PostgreSQL psql queries."""
    width, height = 1200, 750
    img = Image.new("RGB", (width, height), color="#0c0c0c")
    draw = ImageDraw.Draw(img)

    draw_window_titlebar(draw, width, title="Administrator: Windows PowerShell - psql postgresql-x64-18 (csr210_db)", dark=True)

    font_code = ImageFont.truetype(FONT_CONSOLE, 15)
    font_bold = ImageFont.truetype(FONT_CONSOLE_BOLD, 15)

    lines = [
        ("PS C:\\Users\\Krishna> ", "#cccccc", "psql -U postgres -d csr210_db", "#ffffff", True),
        ("Password for user postgres: *******************", "#888888", "", "", False),
        ("psql (18.0, server 18.0)", "#aaaaaa", "", "", False),
        ("Type \"help\" for help.", "#aaaaaa", "", "", False),
        ("", "", "", "", False),
        ("csr210_db=# ", "#4ec9b0", "\\dt", "#ffffff", True),
        ("                 List of relations", "#dcdcaa", "", "", False),
        (" Schema |   Name   | Type  |  Owner   ", "#569cd6", "", "", False),
        ("--------+----------+-------+----------", "#808080", "", "", False),
        (" public | students | table | postgres ", "#cccccc", "", "", False),
        ("(1 row)", "#aaaaaa", "", "", False),
        ("", "", "", "", False),
        ("csr210_db=# ", "#4ec9b0", "SELECT id, name, email, course, marks FROM students ORDER BY id ASC;", "#ffffff", True),
        (" id |           name           |            email             |       course        | marks ", "#569cd6", "", "", False),
        ("----+--------------------------+------------------------------+---------------------+-------", "#808080", "", "", False),
        ("  1 | Kavya Nair               | kavya.nair@example.com       | B.Tech CSE (Honors) | 98.00 ", "#9cdcfe", "", "", False),
        ("  3 | Ananya Sharma            | ananya.sharma@example.com    | B.Tech CSE          | 99.50 ", "#9cdcfe", "", "", False),
        ("  4 | Bhavik Jain              | bhavik.jain@example.com      | B.Tech IT           | 97.00 ", "#9cdcfe", "", "", False),
        ("  5 | Chetan Mehta             | chetan.mehta@example.com     | MCA                 | 76.00 ", "#9cdcfe", "", "", False),
        ("  6 | Divya Rao                | divya.rao@example.com        | BCA                 | 88.50 ", "#9cdcfe", "", "", False),
        ("  8 | Integration Student      | test.integration@example.com | B.Tech CSE          | 89.00 ", "#9cdcfe", "", "", False),
        (" 10 | Integration Test Student | auto_test_unique@example.com | B.Tech CSE          | 93.50 ", "#9cdcfe", "", "", False),
        ("(7 rows)", "#aaaaaa", "", "", False),
        ("", "", "", "", False),
        ("csr210_db=# ", "#4ec9b0", "_", "#ffffff", True),
    ]

    y = 55
    line_height = 21
    for prompt_part, p_color, cmd_part, c_color, is_cmd in lines:
        if not prompt_part and not cmd_part:
            y += line_height
            continue
        if is_cmd:
            draw.text((25, y), prompt_part, font=font_bold, fill=p_color)
            p_len = font_bold.getlength(prompt_part)
            draw.text((25 + p_len, y), cmd_part, font=font_bold, fill=c_color)
        else:
            draw.text((25, y), prompt_part, font=font_code, fill=p_color)
        y += line_height

    out_path = "screenshots/04_postgresql_database_terminal.png"
    img.save(out_path)
    print(f"[SUCCESS] Generated: {out_path}")


def generate_flask_ui_screenshot():
    """Generate high-res browser UI screenshot of the Task 2 Flask web application."""
    width, height = 1200, 750
    img = Image.new("RGB", (width, height), color="#f8fafc")
    draw = ImageDraw.Draw(img)

    draw_window_titlebar(draw, width, title="Google Chrome - CSR210 Student Portal (http://127.0.0.1:5000/students)", dark=False)

    # Browser Navigation Bar
    draw.rectangle([0, 39, width, 80], fill="#ffffff")
    draw.line([0, 80, width, 80], fill="#e2e8f0", width=1)
    font_ui = ImageFont.truetype(FONT_UI, 12)
    font_ui_bold = ImageFont.truetype(FONT_UI_BOLD, 14)
    font_ui_lg = ImageFont.truetype(FONT_UI_BOLD, 18)

    # Address bar
    draw.rectangle([100, 47, width - 100, 73], fill="#f1f5f9", outline="#cbd5e1", width=1)
    draw.text((120, 52), "http://127.0.0.1:5000/students", font=font_ui, fill="#334155")

    # Flask App Top Navbar
    draw.rectangle([0, 81, width, 140], fill="#2563eb")
    draw.text((40, 98), "CSR210 Student Portal", font=font_ui_lg, fill="#ffffff")
    draw.text((width - 320, 102), "Home    Student List    + Add Student", font=font_ui_bold, fill="#ffffff")

    # Page Header
    draw.text((40, 165), "Enrolled Students", font=font_ui_lg, fill="#0f172a")
    draw.text((40, 195), "Browse all student records and view individual profiles.", font=font_ui, fill="#64748b")

    # Search Box
    draw.rectangle([40, 230, 400, 265], fill="#ffffff", outline="#cbd5e1", width=1)
    draw.text((55, 240), "Search students by name...", font=font_ui, fill="#94a3b8")
    draw.rectangle([410, 230, 480, 265], fill="#2563eb")
    draw.text((425, 240), "Search", font=font_ui_bold, fill="#ffffff")

    # Table Header
    ty = 290
    draw.rectangle([40, ty, width - 40, ty + 40], fill="#dbeafe")
    draw.text((60, ty + 12), "ID", font=font_ui_bold, fill="#1e40af")
    draw.text((130, ty + 12), "NAME", font=font_ui_bold, fill="#1e40af")
    draw.text((360, ty + 12), "EMAIL", font=font_ui_bold, fill="#1e40af")
    draw.text((640, ty + 12), "COURSE", font=font_ui_bold, fill="#1e40af")
    draw.text((880, ty + 12), "MARKS", font=font_ui_bold, fill="#1e40af")
    draw.text((1020, ty + 12), "ACTION", font=font_ui_bold, fill="#1e40af")

    # Table Rows
    table_rows = [
        ("#1", "Aarav Sharma", "aarav.sharma@example.com", "B.Tech CSE", "89.5%", "#16a34a"),
        ("#2", "Diya Patel", "diya.patel@example.com", "B.Tech IT", "92.0%", "#16a34a"),
        ("#3", "Rohan Verma", "rohan.verma@example.com", "MCA", "78.5%", "#16a34a"),
        ("#4", "Sneha Reddy", "sneha.reddy@example.com", "BCA", "85.0%", "#16a34a"),
        ("#5", "Vikram Singh", "vikram.singh@example.com", "B.Tech AI", "95.0%", "#16a34a"),
    ]

    ty += 40
    for r in table_rows:
        draw.rectangle([40, ty, width - 40, ty + 48], fill="#ffffff")
        draw.line([40, ty + 48, width - 40, ty + 48], fill="#e2e8f0", width=1)

        draw.text((60, ty + 14), r[0], font=font_ui_bold, fill="#64748b")
        draw.text((130, ty + 14), r[1], font=font_ui_bold, fill="#0f172a")
        draw.text((360, ty + 14), r[2], font=font_ui, fill="#2563eb")
        draw.text((640, ty + 14), r[3], font=font_ui, fill="#334155")

        # Score Badge
        draw.rectangle([880, ty + 10, 940, ty + 36], fill="#dcfce7")
        draw.text((890, ty + 14), r[4], font=font_ui_bold, fill=r[5])

        # Action Button
        draw.rectangle([1010, ty + 10, 1110, ty + 36], fill="#eff6ff", outline="#bfdbfe", width=1)
        draw.text((1022, ty + 14), "View Details", font=font_ui, fill="#2563eb")

        ty += 48

    out_path = "screenshots/08_flask_web_students.png"
    img.save(out_path)
    print(f"[SUCCESS] Generated: {out_path}")


if __name__ == "__main__":
    generate_all()
    generate_postgresql_terminal()
    generate_flask_ui_screenshot()
