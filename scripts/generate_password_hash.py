"""
Script para generar hash bcrypt de contraseñas.
Uso: python -m scripts.generate_password_hash 'tu_contraseña'
"""
import bcrypt
import sys

def generate_hash(password: str, rounds: int = 12) -> str:
    """
    Genera hash bcrypt de una contraseña.
    
    Args:
        password: Contraseña en texto plano
        rounds: Número de rondas de sal (default: 12, más alto = más seguro pero más lento)
    
    Returns:
        Hash bcrypt como string
    """
    salt = bcrypt.gensalt(rounds=rounds)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def main():
    if len(sys.argv) < 2:
        print("\n=== Generador de Hash de Contraseña ===")
        print("\nUso: python -m scripts.generate_password_hash 'tu_contraseña'")
        print("\nEjemplo:")
        print("  python -m scripts.generate_password_hash 'MiContraseñaSegura123'")
        sys.exit(1)
    
    password = sys.argv[1]
    
    if len(password) < 8:
        print("\n⚠️  ADVERTENCIA: Se recomienda usar una contraseña de al menos 8 caracteres.")
        print("    Para mayor seguridad, incluye mayúsculas, minúsculas, números y símbolos.\n")
    
    print("\nGenerando hash (esto puede tomar unos segundos)...")
    hash_result = generate_hash(password)
    
    print("\n" + "="*70)
    print("Hash generado exitosamente:")
    print("="*70)
    print(f"\n{hash_result}\n")
    print("="*70)
    print("\nAgrega esta línea a tu archivo .env:")
    print("="*70)
    print(f"\nAPP_PASSWORD_HASH={hash_result}\n")
    print("="*70)
    print("\nPara Streamlit Cloud (secrets.toml):")
    print("="*70)
    print(f'\nAPP_PASSWORD_HASH = "{hash_result}"\n')
    print("="*70)
    print("\n✅ Hash generado correctamente. Copia y pega la línea correspondiente.")
    print("⚠️  IMPORTANTE: Nunca compartas este hash públicamente en tu repositorio.\n")


if __name__ == "__main__":
    main()
