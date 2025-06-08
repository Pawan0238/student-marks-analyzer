import tkinter as tk
from tkinter import messagebox, filedialog
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

students = []

def calculate_grade(percentage):
    if percentage >= 90:
        return 'A+'
    elif percentage >= 80:
        return 'A'
    elif percentage >= 70:
        return 'B'
    elif percentage >= 60:
        return 'C'
    elif percentage >= 50:
        return 'D'
    else:
        return 'F'

def add_student():
    name = name_entry.get()
    marks = marks_entry.get()

    if not name or not marks:
        messagebox.showwarning("Input Error", "Please enter both name and marks.")
        return

    try:
        marks_list = list(map(float, marks.split(',')))
    except ValueError:
        messagebox.showwarning("Input Error", "Please enter valid marks separated by commas.")
        return

    total = sum(marks_list)
    percentage = total / len(marks_list)
    grade = calculate_grade(percentage)

    student = {
        'name': name,
        'marks': marks_list,
        'total': total,
        'percentage': percentage,
        'grade': grade
    }
    students.append(student)
    messagebox.showinfo("Success", f"Record added for {name}.")
    name_entry.delete(0, tk.END)
    marks_entry.delete(0, tk.END)

def show_report():
    if not students:
        messagebox.showinfo("No Data", "No student data to display.")
        return

    report = ""
    for s in students:
        report += f"Name       : {s['name']}\n"
        report += f"Marks      : {s['marks']}\n"
        report += f"Total      : {s['total']}\n"
        report += f"Percentage : {s['percentage']:.2f}%\n"
        report += f"Grade      : {s['grade']}\n\n"

    topper = max(students, key=lambda x: x['percentage'])
    lowest = min(students, key=lambda x: x['percentage'])

    report += f"Topper        : {topper['name']} ({topper['percentage']:.2f}%)\n"
    report += f"Lowest Scorer : {lowest['name']} ({lowest['percentage']:.2f}%)"

    messagebox.showinfo("Student Report", report)

def save_report():
    if not students:
        messagebox.showinfo("No Data", "No student data to save.")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".pdf", title="Save Report As PDF",
                                             filetypes=[("PDF files", "*.pdf")])
    if not file_path:
        return

    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4
    y = height - 50

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "Student Marks Report")
    y -= 30

    c.setFont("Helvetica", 12)

    for student in students:
        c.drawString(50, y, f"Name       : {student['name']}")
        y -= 20
        c.drawString(50, y, f"Marks      : {student['marks']}")
        y -= 20
        c.drawString(50, y, f"Total      : {student['total']}")
        y -= 20
        c.drawString(50, y, f"Percentage : {student['percentage']:.2f}%")
        y -= 20
        c.drawString(50, y, f"Grade      : {student['grade']}")
        y -= 30

        if y < 100:
            c.showPage()
            y = height - 50
            c.setFont("Helvetica", 12)

    topper = max(students, key=lambda x: x['percentage'])
    lowest = min(students, key=lambda x: x['percentage'])

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, f"Topper        : {topper['name']} ({topper['percentage']:.2f}%)")
    y -= 20
    c.drawString(50, y, f"Lowest Scorer : {lowest['name']} ({lowest['percentage']:.2f}%)")

    c.save()
    messagebox.showinfo("Success", "Report saved as PDF successfully!")

def show_graph():
    if not students:
        messagebox.showinfo("No Data", "No data to plot.")
        return

    names = [s['name'] for s in students]
    percentages = [s['percentage'] for s in students]

    plt.figure(figsize=(10, 5))
    plt.bar(names, percentages, color='skyblue')
    plt.xlabel('Student Name')
    plt.ylabel('Percentage')
    plt.title('Student Performance')
    plt.ylim(0, 100)
    plt.grid(axis='y')
    plt.tight_layout()
    plt.show()

# GUI Setup
root = tk.Tk()
root.title("Student Marks Analyzer")
root.geometry("500x400")
root.config(bg="#f0f4f7")

frame = tk.Frame(root, padx=20, pady=20, bg="#ffffff", bd=2, relief="groove")
frame.pack(pady=30)

# Labels and Entries
tk.Label(frame, text="Student Name:", bg="#ffffff").grid(row=0, column=0, pady=5, sticky='e')
name_entry = tk.Entry(frame, width=30)
name_entry.grid(row=0, column=1, pady=5)

tk.Label(frame, text="Marks (comma separated):", bg="#ffffff").grid(row=1, column=0, pady=5, sticky='e')
marks_entry = tk.Entry(frame, width=30)
marks_entry.grid(row=1, column=1, pady=5)

# Buttons
tk.Button(frame, text="Add Student", command=add_student, bg="#4caf50", fg="white", width=20).grid(row=2, columnspan=2, pady=10)
tk.Button(frame, text="Show Report", command=show_report, width=20).grid(row=3, columnspan=2, pady=5)
tk.Button(frame, text="Save Report to File", command=save_report, width=20).grid(row=4, columnspan=2, pady=5)
tk.Button(frame, text="Show Percentage Graph", command=show_graph, width=20).grid(row=5, columnspan=2, pady=5)

root.mainloop()
