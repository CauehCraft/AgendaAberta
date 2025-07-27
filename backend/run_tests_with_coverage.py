#!/usr/bin/env python
"""
Script para executar os testes com cobertura.
Uso: python run_tests_with_coverage.py
"""

import os
import sys
import coverage
import django
from django.conf import settings
from django.test.utils import get_runner

if __name__ == "__main__":
    # Iniciar cobertura
    cov = coverage.Coverage()
    cov.start()
    
    # Configurar Django
    os.environ['DJANGO_SETTINGS_MODULE'] = 'agenda_aberta.settings'
    django.setup()
    
    # Executar testes
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=2, interactive=True)
    failures = test_runner.run_tests(["core"])
    
    # Parar cobertura e gerar relatório
    cov.stop()
    cov.save()
    
    print("\nCoverage Report:")
    cov.report()
    
    # Gerar relatório HTML
    cov.html_report()
    
    print("\nHTML report generated in htmlcov/ directory")
    
    # Sair com código de erro se houver falhas
    sys.exit(bool(failures))