from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime

class ReportGenerator:
    def generar_pdf(self, datos, filename="reporte_institucional.pdf"):
        c = canvas.Canvas(filename, pagesize=letter)
        width, height = letter
        
        # Encabezado
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, height - 50, "ESCUELA MILITAR DE INGENIERÍA")
        c.setFont("Helvetica", 12)
        c.drawString(50, height - 70, "Reporte de Percepción Institucional")
        
        # Fecha
        c.drawString(50, height - 100, f"Fecha: {datetime.now().strftime('%d/%m/%Y')}")
        
        # Resumen
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, height - 140, "1. Resumen Ejecutivo")
        c.setFont("Helvetica", 11)
        texto = f"Se analizaron {datos['total']} publicaciones. "
        texto += f"Percepción positiva: {datos['positivos']} ({datos['tasa_positiva']:.1f}%). "
        texto += f"Percepción negativa: {datos['negativos']} ({datos['tasa_negativa']:.1f}%)."
        c.drawString(50, height - 160, texto)
        
        # Factores
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, height - 200, "2. Factores de Percepción")
        y = height - 220
        for factor, menciones in datos.get('factores', {}).items():
            c.drawString(50, y, f"- {factor}: {menciones} menciones")
            y -= 20
        
        c.save()
        return filename