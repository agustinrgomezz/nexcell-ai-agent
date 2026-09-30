from agente import AgenteNexcell

def iniciar_chat():
    print("Iniciando Sistema de Asistencia Nexcell...")
    agente = AgenteNexcell()
    
    print("\n" + "="*50)
    print("NexcellBot: ¡Hola! Soy el asistente virtual de Nexcell.")
    print("NexcellBot: ¿En qué te puedo ayudar hoy? (Escribí 'salir' para terminar)")
    print("="*50 + "\n")
    
    while True:
        usuario_input = input("Vos: ")
        
        if usuario_input.lower() in ['salir', 'exit', 'quit']:
            print("\nNexcellBot: ¡Gracias por visitar Nexcell! Hasta luego.")
            break
            
        if not usuario_input.strip():
            continue
            
        print("Pensando...")
        respuesta = agente.procesar_mensaje(usuario_input)
        print(f"\nNexcellBot: {respuesta}\n")

if __name__ == "__main__":
    iniciar_chat()