import speech_recognition as sr
import datetime


programming_languages = ["python", "java", "c++"]
r = sr.Recognizer()
main_code = ""
final_code = ""
beginning_code = ""
imports = []
methods = {}
method_texts = []
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


def method_parameter_processor(text_words, from_command):
        param_text = ""
        params = {}
        param_count = 0
        try:
            for i in range(len(text_words)):
                if text_words[i] == "parameter" or text_words[i] == "argument":
                    par_type = text_words[text_words[i:].index("type") + 1]
                    par_value = "_".join(text_words[text_words[i:].index("value")+1 : text_words[i:].index("type")])
                    params[str(param_count)] = {"value": par_value, "type": par_type}
                    param_count += 1
                i += 1
            for key, param in params:
                if not list(params.keys()).index(key) == 0:
                    param_text += ", "
                param_text += f"\"{param['value']}\"" if param['type'] == "string" else f"{param['value']}"
            return param_text
        except:
            print(f"[-] Invalid usage of the command: {from_command}")
            raise BaseException


def add_imports(code, programming_language):
    import_string = ""
    for item in imports:
        if programming_language == "java":
            import_string += f"import {item};\n"
        elif programming_language == "c++":
            import_string += f"#include <{item}>\n"
        elif programming_language == "python":
            import_string += f"import {item}\n"
    return import_string


if __name__ == '__main__':
    user_choice = input(f"[!] What programming do you wish to choose (java, python, c++)? ").lower()
    if user_choice not in programming_languages:
        print(f"[-] Programming language {user_choice} is not supported\nExiting the program")
        exit(1)
    if user_choice == "java":
        beginning_code += """class MyProgram {\npublic static void main(String[] args) {\n\t\t// Java Code Here\n\t\t"""
    elif user_choice == "c++":
        beginning_code += """#include <iostream>\n\nint main() {\n\t// C++ Code Here\n\t"""
    while True:
        text = listen()
        print(text + "\n")
        text_words = text.split()
        if text.startswith("method edit"):
            # TODO
            method_name = text_words[text_words.index("method")+1]
            # Here we do the works on the method that the user said they want to change
            pass
        elif text.startswith("operation"):
            # TODO
            pass
        elif text.startswith("method call"):
            method_text = ""
            try:
                method_name = "_".join(text_words[text_words.index("name")+1 : text_words.index("name")+3])
                method_text += f"{method_name}({method_parameter_processor(text, from_command='method call')}"
            except:
                continue
            if user_choice == "java":
                method_text += ");"
                main_code += f"{method_text}\n\t\t"
            elif user_choice == "c++":
                method_text += ");"
                main_code += f"{method_text}\n\t"
            elif user_choice == "python":
                method_text += ")"
                main_code += f"{method_text}\n"
        elif text.startswith("new method"):
            # TODO
            method_text = ""
            method_name = text_words[text_words.index("name")+1]
            if "parameters" in text_words:
                method_parameters = text_words[text_words.index("parameter")+1]
            if "return" in text_words:
                method_returns = text_words[text_words.index("return")+1]
            main_code = method_text + "\n\n\n" + main_code

        elif text.startswith("new variable"):
            try:
                var_name = text_words[text_words.index("name")+1]
                var_value = text_words[text_words.index("value")+1]
                var_type = text_words[text_words.index("type")+1]
            except:
                print("[-] Invalid usage of the command: New variable")
                continue
            code_variables[var_name] = {
                'value': var_value,
                'type': var_type
            }
            if var_type == "string":
                if user_choice == "java":
                    main_code = main_code + f"""String {var_name} = \"{var_value}\";\n\t\t"""
                elif user_choice == "c++":
                    if "<string>" not in imports:
                        imports.append("string")
                    main_code = main_code + f"""string {var_name} = \"{var_value}\";\n\t"""
                elif user_choice == "python":
                    main_code = main_code + f"""{var_name} = \"{var_value}\"\n"""
            elif var_type == "number":
                if user_choice == "java":
                    main_code = main_code + f"""int {var_name} = {var_value};\n\t\t"""
                elif user_choice == "c++":
                    main_code = main_code + f"""int {var_name} = {var_value};\n\t"""
                elif user_choice == "python":
                    main_code = main_code + f"""{var_name} = {var_value}\n"""
            print("[+] Added new Variable")
        elif text.startswith("print"):
            if "variable" in text_words:
                print_object = "_".join(text_words[text_words.index("name")+1:])
                if print_object in code_variables:
                    if user_choice == "java":
                        main_code = main_code + f"""System.out.println({print_object});\n\t\t"""
                    elif user_choice == "c++":
                        main_code = main_code + f"""std::cout << {print_object};\n\t"""
                    elif user_choice == "python":
                        main_code = main_code + f"""print({print_object})\n"""
                else:
                    print(f"[-] Variable {print_object} does not exist")
            else:
                print_object = " ".join(text_words[text_words.index("print")+1:])
                if user_choice == "java":
                    main_code = main_code + f"System.out.println(\"{print_object}\");\n\t\t"
                elif user_choice == "c++":
                    main_code = main_code + f"std::cout << \"{print_object}\";\n\t"
                elif user_choice == "python":
                    main_code = main_code + f"print(\"{print_object}\")\n"

            print("[+] Added print")
        elif text == "exit the program" or text == "stop the program" or text == "stop listening":
            print("[*] Stopping the program...")
            break

    print("[+] Adding the imports...")
    beginning_code = add_imports(main_code, user_choice) + beginning_code
    print("[+] Finalizing the code...")
    if user_choice == "java":
        final_code = beginning_code + main_code + "\n\t}\n}"
    elif user_choice == "c++":
        final_code = beginning_code + main_code + "\n}"
    elif user_choice == "python":
        final_code = beginning_code + main_code + "\n"

    file_name = f"output_file_{datetime.datetime.now().strftime('%Y_%m_%d-%I_%M_%S_%p')}.{'py' if user_choice == 'python' else ('java' if user_choice == 'java' else 'cpp')}"
    print(f"writing the log file: {file_name}")
    with open(file_name, "w") as file:
        file.write(final_code)
    print("[!] Exiting the program...")
