#include <windows.h>
#include <stdio.h>

// Programme réalisé par Houguet Maxence et Coupry Baptiste
void* get_addr_fonction(const char* module_dll, const char* fonction) {

    // On charge ici le module correspondant avec LoadLibraryA
    HMODULE module_dll_charge = LoadLibraryA(module_dll);
    // on obtient l'@ avec GetProcAddress qui recupere l’adresse d’une fonction exportee
    void * addr_fonction = GetProcAddress(module_dll_charge, fonction);

    return addr_fonction;
}

int main(int argc, char* argv[]) {

    if (argc < 3) {
        printf("Utilisation du prog : %s <module_dll> <fonction>", argv[0]);
        exit(0);
    }

    const char* module_dll = argv[1];
    const char* fonction = argv[2];

    void *addr_function = get_addr_fonction(module_dll, fonction);

    if (addr_function) {
        printf("Adresse de %s dans %s : %p\n", fonction, module_dll, addr_function);
    }
    else {
        printf("Adresse de %s dans %s impossible à retrouver\n", fonction, module_dll);
    }

    return 0;
}

/* Notes :

LoadLibraryA : 
- Charge le module spécifié dans l’espace d’adressage du processus appelant
- Structure :
HMODULE LoadLibraryA(
  [in] LPCSTR lpLibFileName
);

GetProcAddress :
- Récupère l’adresse d’une fonction exportée (également appelée procédure) ou d’une variable à partir
 de la bibliothèque de liens dynamiques (DLL) spécifiée.
- Structure :
FARPROC GetProcAddress(
  [in] HMODULE hModule,
  [in] LPCSTR  lpProcName
);

*/
