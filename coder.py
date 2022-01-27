import speech_recognition as sr
import datetime


programming_languages = ["python", "java", "c++"]
r = sr.Recognizer()
final_code = ""
imports = []
code_variables = {}


def listen():
    query = ""
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.2)
        print("Listening...")
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en')

    except:
        print("Sorry i didn't catch that...")
    return query.lower()


def ln(tabs=0):
    s = ""
    for i in range(tabs):
        s = s + "\t"
    s = s + "\n"
    return s


def add_imports(code, programming_language):
    import_string = """"""
    for item in imports:
        if programming_language == "java":
            import_string += f"import {item};\n"
        elif programming_language == "c++":
            import_string += f"#include <{item}>\n"
        elif programming_language == "python":
            import_string += f"import {item}\n"
    code = f"{import_string}\n\n{code}"
    return code


if __name__ == '__main__':
    user_choice = input(f"[!] What programming do you wish to choose (java, python, c++)? ").lower()
    if user_choice not in programming_languages:
        print(f"[-] Programming language {user_choice} is not supported\nExiting the program")
        exit(1)
    if user_choice == "java":
        final_code = final_code + """class MyProgram {\npublic static void main(String[] args) {\n\t\t// Java Code Here\n\t\t"""
    elif user_choice == "c++":
        final_code = final_code + """#include <iostream>\n\nint main() {\n\t// C++ Code Here\n\t"""
    while True:
        text = listen()
        print(text + "\n")
        text_words = text.split()
        if "operation" in text:
            pass
        elif "method call" in text:
            pass
        elif "new method" in text:
            pass
        elif "new variable" in text:
            var_name = text_words[text_words.index("name")+1]
            var_value = text_words[text_words.index("value")+1]
            var_type = text_words[text_words.index("type")+1]
            code_variables[var_name] = {
                'value': var_value,
                'type': var_type
            }
            if var_type == "string":
                if user_choice == "java":
                    final_code = final_code + f"""String {var_name} = "{var_value}";\n\t\t"""
                elif user_choice == "c++":
                    if "<string>" not in imports:
                        imports.append("string")
                    final_code = final_code + f"""string {var_name} = "{var_value}";\n\t"""
                elif user_choice == "python":
                    final_code = final_code + f"""{var_name} = "{var_value}"\n"""
            elif var_type == "integer":
                if user_choice == "java":
                    final_code = final_code + f"""int {var_name} = {var_value};\n\t\t"""
                elif user_choice == "c++":
                    final_code = final_code + f"""int {var_name} = {var_value};\n\t"""
                elif user_choice == "python":
                    final_code = final_code + f"""{var_name} = "{var_value}"\n"""
            print("[+] Added new Variable")
        elif "print" in text_words:
            if "variable" in text_words:
                print_object = "_".join(text_words[text_words.index("name")+1:])
                if print_object in code_variables:
                    if user_choice == "java":
                        final_code = final_code + f"""System.out.println({print_object});\n\t\t"""
                    elif user_choice == "c++":
                        final_code = final_code + f"""std::cout << {print_object};\n\t"""
                    elif user_choice == "python":
                        final_code = final_code + f"""print({print_object})\n"""
                else:
                    print(f"[-] Variable {print_object} does not exist")
            else:
                print_object = " ".join(text_words[text_words.index("print")+1:])
                if user_choice == "java":
                    final_code = final_code + f"""System.out.println("{print_object}");\n\t\t"""
                elif user_choice == "c++":
                    final_code = final_code + f"""std::cout << "{print_object}";\n\t"""
                elif user_choice == "python":
                    final_code = final_code + f"""print("{print_object}")\n"""

            print("[+] Added print")
        elif text == "exit the program" or text == "stop the program" or text == "stop listening":
            print("[*] Stopping the program...")
            break

    print("[+] Finalizing the code...")
    print("[+] Adding the imports...")
    final_code = add_imports(final_code, user_choice)
    if user_choice == "java":
        final_code = final_code + """\n\t}\n}"""
    elif user_choice == "c++":
        final_code = final_code + """\n}"""
    file_name = f"output_file_{datetime.datetime.now().strftime('%Y_%m_%d-%I_%M_%S_%p')}.{'py' if user_choice == 'python' else ('java' if user_choice == 'java' else 'cpp')}"
    print(f"writing the log file: {file_name}")
    with open(file_name, "w") as file:
        file.write(final_code)
    print("[!] Exiting the program...")
