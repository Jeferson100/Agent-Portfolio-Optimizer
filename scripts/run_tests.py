#!/usr/bin/env python3
"""
Script para executar testes do projeto Agent Portfolio Optimizer.
"""

import argparse
import subprocess
import sys
from pathlib import Path


def run_command(cmd: list[str], description: str) -> bool:
    """Executa um comando e retorna True se bem-sucedido."""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"✅ {description} - Sucesso")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Falhou")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(description="Executa testes do projeto")
    parser.add_argument("--unit", action="store_true", help="Executa apenas testes unitários")
    parser.add_argument("--integration", action="store_true", help="Executa apenas testes de integração")
    parser.add_argument("--coverage", action="store_true", help="Executa testes com cobertura")
    parser.add_argument("--lint", action="store_true", help="Executa linting")
    parser.add_argument("--type-check", action="store_true", help="Executa verificação de tipos")
    parser.add_argument("--all", action="store_true", help="Executa todos os checks")
    parser.add_argument("--fast", action="store_true", help="Executa apenas testes rápidos")
    
    args = parser.parse_args()
    
    # Verifica se estamos no diretório correto
    if not Path("pyproject.toml").exists():
        print("❌ Execute este script a partir do diretório raiz do projeto")
        sys.exit(1)
    
    success = True
    
    if args.all or args.lint:
        success &= run_command(["uv", "run", "ruff", "check", "src/"], "Verificação de linting")
        success &= run_command(["uv", "run", "ruff", "format", "--check", "src/"], "Verificação de formatação")
    
    if args.all or args.type_check:
        success &= run_command(["uv", "run", "mypy", "src/"], "Verificação de tipos")
    
    # Testes
    if args.unit:
        success &= run_command(["uv", "run", "pytest", "-m", "unit", "-v"], "Testes unitários")
    elif args.integration:
        success &= run_command(["uv", "run", "pytest", "-m", "integration", "-v"], "Testes de integração")
    elif args.fast:
        success &= run_command(["uv", "run", "pytest", "-m", "not slow", "-v"], "Testes rápidos")
    elif args.coverage:
        success &= run_command([
            "uv", "run", "pytest", 
            "--cov=src/portfolio_optimizer", 
            "--cov-report=html", 
            "--cov-report=term-missing",
            "--cov-fail-under=70"
        ], "Testes com cobertura")
    elif args.all:
        success &= run_command([
            "uv", "run", "pytest", 
            "--cov=src/portfolio_optimizer", 
            "--cov-report=html", 
            "--cov-report=term-missing",
            "--cov-fail-under=70",
            "-v"
        ], "Todos os testes com cobertura")
    else:
        success &= run_command(["uv", "run", "pytest", "-v"], "Todos os testes")
    
    if success:
        print("\n🎉 Todos os checks passaram!")
        sys.exit(0)
    else:
        print("\n💥 Alguns checks falharam!")
        sys.exit(1)


if __name__ == "__main__":
    main()