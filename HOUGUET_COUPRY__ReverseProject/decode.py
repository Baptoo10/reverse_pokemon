import sys
import base64

# Programme réalisé par Houguet Maxence et Coupry Baptiste
def read_bytes_from_executable(executable_path, address, length):
    with open(executable_path, 'rb') as f:
        f.seek(address)
        return f.read(length)

def write_decoded_script(decoded_script, output_path):
    with open(output_path, 'w', encoding="utf-16") as f:
        f.write(decoded_script)


def desobfucation(data):
    texte = ""
    lines = data.split("\n")
    variables = {"":""}
    variables.popitem()
    
    
    # Première ligne
    line = lines[0].split(";")
    
    for i in range(0,len(line)):
        if("$"in line[i] and "=" in line[i]):
            
            # Déclaration de variable
            if(" " not in line[i] and "+" not in line[i]):
                operation = line[i].split("=")
                if(int(operation[1]) > 23):
                    variables[operation[0]]=chr(int(operation[1]))
                else:
                    variables[operation[0]]=int(operation[1])
                    
            # Opération d'addition
            if(" " not in line[i] and "+" in line[i]):
                operation = line[i].split("=")
                
                operation[1] = operation[1].replace("(","").replace("[char]","").replace(")","")
                
                var_add = operation[1].split("+")
                added = ""
                for j in range(0,len(var_add)):
                    added += (variables[var_add[j]])
                
                variables[operation[0]] = added
                
            # Commande
            if(" " in line[i]):
                operation = line[i].split("=")
                
                first_command = operation[1]
                for cle in variables:
                    if cle in first_command:
                        first_command=first_command.replace(cle,variables.get(cle))
                
                variables[operation[0].replace(" ", "")] = first_command
                            
    # Deuxième ligne
    
    line = lines[1]
    line = line.split("=",1)
    line[0]=line[0].replace(" ","")
    variable = line[0]
    command = line[1]
    for cle in variables:
        if cle in command:
            command = command.replace(cle,variables[cle])
    
    variables[variable] = command
    
    # Troisieme ligne
    line = lines[2]
    line = line.split('=',1)
    line[0]=line[0].replace(" ","")
    variable = line[0]
    command = line[1]
    
    for cle in variables:
        if cle in command:
            
            command = command.replace(cle,variables[cle])
            
    
    variables[variable] = command
    
    # Quatrieme ligne
    line = lines[4]
    line=line.replace("[char]","").replace("+","")
    for cle in variables:
        if cle in line:
            try:
                line = line.replace(cle,variables[cle])
            except:
                line = line.replace(cle,str(variables[cle]))
    texte += line + "\n"
    
    
    # Cinquieme ligne
    line = lines[5]
    line = line.replace("[char]","").replace("+","")
    
    operation = line.split("=")
    line = operation[1].split(" ")
    
    for i in range(0,len(line)):    
        for cle in variables:
            if cle in line[i]:
                if i == 1:
                    try:
                        line[i] = line[i].replace(cle,str(int(variables[cle])))
                    except:
                        line[i] = line[i].replace(cle,str(ord(variables[cle])))
                else:
                    line[i] = line[i].replace(cle,variables[cle])
    operation[1] = "".join(line)
    variables[operation[0]]=operation[1]

    texte += operation[0]
    texte += " = "
    texte += operation[1]
    texte += "\n"

    # Sixième ligne
    for i in range(6,40):
        texte += lines[i] +"\n"
    
    
    # ligne 41
    line = lines[40]
    line = line.split(" ")
    line[2] = line[2].replace("[char]","").replace("+","")
    for cle in variables:
        if cle in line[2]:
            try:
                line[2] = line[2].replace(cle,variables[cle])
            except:
                line[2] = line[2].replace(cle,str(variables[cle]))
                
    for cle in variables:
        if cle in line[1]:
            try:
                line[1] = line[1].replace(cle,variables[cle])
            except:
                line[1] = line[1].replace(cle,str(variables[cle]))
                
    texte += line[0] +" " + line[1] + " " + line[2] + "\n" + lines[41] + "\n"
    print(texte)
    print(variables)
    return texte

        
def decode_data(data,length,word):
        
    i=0
    while(i<length):
        try:
            data[i] ^= word[i%7]
            data[i+1] ^= word[int(i+((-7 * ((i+1)//7)) + 1))%7]
            data[i+2] ^= word[int(i+((-7 * ((i+2)//7)) + 2))%7]
            data[i+3] ^= word[int(i+((-7 * ((i+3)//7)) + 3))%7]
            data[i+4] ^= word[int(i+((-7 * ((i+4)//7)) + 4))%7]
            data[i+5] ^= word[int(i+((-7 * ((i+5)//7)) + 5))%7]
            
            i = i + 6
        except:
            return data
            

        
        
    return data

def main():

    if len(sys.argv) == 3:
        executable_path = sys.argv[1] #"pikachu.exe"
        output_script_path = sys.argv[2] #"dracaufeu.ps1"
    else:
        print("decode.py [executable] [sortie]")
        return 0

    # Image_base et l'Offset ce trouve au début du fichier exec
    length = 19392
    address = 0x1400082E0
    image_base = 0x140001000
    offset = 0x800
    
    adr = address - image_base - offset
    
    # Lecture des données
    data = read_bytes_from_executable(executable_path, adr, length) 
    print(data)
    
    print("-----------------------------------------------------------------------------------------")
    print("--------------------------------RESULTAT APRES DECODE_DATA-------------------------------")
    print("-----------------------------------------------------------------------------------------")
    
    dynamax = "dynamax"
    dynamax = bytearray(bytes(dynamax,"utf-8"))
    decoded = decode_data(bytearray(data),length,dynamax)
    print(decoded)
    
    print("-----------------------------------------------------------------------------------------")
    print("-----------------------------------BASE 64 DECODE----------------------------------------")
    print("-----------------------------------------------------------------------------------------")
    
    data = decoded.decode("utf-8",errors="ignore")
    decoded_data = base64.b64decode(data)
    print(decoded_data)
    
    print("-----------------------------------------------------------------------------------------")
    print("---------------------------------EN UTF 16-----------------------------------------------")
    print("-----------------------------------------------------------------------------------------")

    print_dracaufeu = decoded_data.decode("utf-16",errors="ignore")
    print(print_dracaufeu)

    write_decoded_script(decoded_data.decode("utf-16",errors="ignore"), output_script_path)

    print(f"Script décodé écrit dans {output_script_path}")
    
    print("-----------------------------------------------------------------------------------------")
    print("---------------------------------Desobfuscation--------------------------------------------")
    print("-----------------------------------------------------------------------------------------")
    try:
        data = desobfucation(decoded_data.decode("utf-16",errors="ignore"))
        write_decoded_script(data,"dracaufeu.txt")
    except:
        print("Erreur lors de la desobfuscation")
    
    

main()