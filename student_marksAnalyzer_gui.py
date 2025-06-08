import tkinter as tk
from tkinter import messagebox, filedialog
import matplotlib.pyplot as plt

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

students = []

def add_student():
    try:
        name = entry_name.get().strip()
        marks_str = entry_marks.get().strip()
        if not name:
            messagebox.showerror("Input Error", "Please enter student name.")
            return
        if not marks_str:
            messagebox.showerror("Input Error", "Please enter marks separated by commas.")
            return

        marks_list = [float(mark.strip()) for mark in marks_str.split(',') if mark.strip()]
        if not marks_list:
            messagebox.showerror("Input Error", "Please enter valid marks.")
            return

        total = sum(marks_list)
        percentage = total / len(marks_list)
        grade = calculate_grade(percentage)

        student = {
            'name': name,
            'total': total,
            'percentage': percentage,
            'grade': grade
        }
        students.append(student)

        # Update result label
        result = f"Added: {name} | Percentage: {percentage:.2f}% | Grade: {grade}"
        label_result.config(text=result)

        # Clear inputs
        entry_name.delete(0, tk.END)
        entry_marks.delete(0, tk.END)

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numeric marks separated by commas.")

def show_report():
    if not students:
        messagebox.showinfo("No Data", "No students added yet.")
        return

    report = "STUDENT REPORT\n" + "="*40 + "\n"
    for s in students:
        report += (f"Name: {s['name']}\n"
                   f"Total Marks: {s['total']}\n"
                   f"Percentage: {s['percentage']:.2f}%\n"
                   f"Grade: {s['grade']}\n"
                   + "-"*40 + "\n")

    # Find topper and lowest scorer
    topper = max(students, key=lambda x: x['percentage'])
    lowest = min(students, key=lambda x: x['percentage'])

    report += f"\n🏆 TOPPER: {topper['name']} with {topper['percentage']:.2f}% ({topper['grade']})\n"
    report += f"📉 LOWEST SCORER: {lowest['name']} with {lowest['percentage']:.2f}% ({lowest['grade']})\n"

    # Show report in messagebox (or could be a popup window)
    messagebox.showinfo("Student Report", report)

def save_report():
    if not students:
        messagebox.showinfo("No Data", "No students added yet.")
        return

    report = "STUDENT REPORT\n" + "="*40 + "\n"
    for s in students:
        report += (f"Name: {s['name']}\n"
                   f"Total Marks: {s['total']}\n"
                   f"Percentage: {s['percentage']:.2f}%\n"
                   f"Grade: {s['grade']}\n"
                   + "-"*40 + "\n")

    topper = max(students, key=lambda x: x['percentage'])
    lowest = min(students, key=lambda x: x['percentage'])

    report += f"\n🏆 TOPPER: {topper['name']} with {topper['percentage']:.2f}% ({topper['grade']})\n"
    report += f"📉 LOWEST SCORER: {lowest['name']} with {lowest['percentage']:.2f}% ({lowest['grade']})\n"

    # Ask for file location
    filepath = filedialog.asksaveasfilename(defaultextension=".txt",
                                            filetypes=[("Text files","*.txt"), ("All files","*.*")])
    if filepath:
        with open(filepath, "w") as f:
            f.write(report)
        messagebox.showinfo("Saved", f"Report saved to:\n{filepath}")

def plot_graph():
    if not students:
        messagebox.showinfo("No Data", "No students added yet.")
        return

    names = [s['name'] for s in students]
    percentages = [s['percentage'] for s in students]

    plt.figure(figsize=(8,5))
    plt.bar(names, percentages, color='skyblue')
    plt.xlabel('Students')
    plt.ylabel('Percentage')
    plt.title('Student Percentages')
    plt.ylim(0, 100)
    plt.grid(axis='y')
    plt.show()

# Tkinter setup
root = tk.Tk()
root.title("Student Marks Analyzer")

tk.Label(root, text="Student Name:").grid(row=0, column=0, padx=10, pady=10, sticky='w')
entry_name = tk.Entry(root, width=30)
entry_name.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Marks (comma separated):").grid(row=1, column=0, padx=10, pady=10, sticky='w')
entry_marks = tk.Entry(root, width=30)
entry_marks.grid(row=1, column=1, padx=10, pady=10)

btn_add = tk.Button(root, text="Add Student", command=add_student)
btn_add.grid(row=2, column=0, columnspan=2, pady=5, sticky='ew')

btn_report = tk.Button(root, text="Show Report", command=show_report)
btn_report.grid(row=3, column=0, pady=5, sticky='ew')

btn_save = tk.Button(root, text="Save Report to File", command=save_report)
btn_save.grid(row=3, column=1, pady=5, sticky='ew')

btn_graph = tk.Button(root, text="Show Percentage Graph", command=plot_graph)
btn_graph.grid(row=4, column=0, columnspan=2, pady=10, sticky='ew')

label_result = tk.Label(root, text="", justify='left', font=('Arial', 12))
label_result.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()
