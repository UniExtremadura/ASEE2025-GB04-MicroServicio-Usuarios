# ============================================================================
# ETAPA 1: Compilador (Builder)
# Propósito: Instalar dependencias y compilar wheels para optimizar la imagen
# ============================================================================
FROM python:3.11-slim as builder

# Establecer variables de entorno para Python
# PYTHONUNBUFFERED: Evita buffering de output (importante para logs en contenedores)
# PYTHONDONTWRITEBYTECODE: Evita generar archivos .pyc (menos espacio en disco)
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Actualizar pip y herramientas de compilación necesarias para dependencias con C extensions
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo en el builder
WORKDIR /build

# Copiar requirements.txt
COPY app/requirements.txt .

# Compilar wheels (binarios precompilados) de todas las dependencias
# Esto acelera la instalación en la etapa final
RUN pip install --upgrade pip setuptools wheel && \
    pip wheel --no-cache-dir --wheel-dir /build/wheels -r requirements.txt


# ============================================================================
# ETAPA 2: Runtime (Imagen Final)
# Propósito: Imagen ligera con solo las dependencias compiladas necesarias
# ============================================================================
FROM python:3.11-slim

# Establecer variables de entorno
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    # Ruta de la aplicación
    APP_HOME=/app

# Instalar solo las librerías de runtime necesarias (sin herramientas de compilación)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Crear usuario no-root para ejecutar la aplicación (mejora seguridad)
# Evita ejecutar la app como root
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Establecer directorio de trabajo
WORKDIR ${APP_HOME}

# Copiar wheels compilados desde la etapa builder
COPY --from=builder /build/wheels /tmp/wheels

# Instalar las dependencias desde los wheels compilados
# Esto es mucho más rápido que compilar en tiempo de ejecución
RUN pip install --upgrade pip && \
    pip install --no-cache /tmp/wheels/* && \
    rm -rf /tmp/wheels

# Copiar la aplicación completa al contenedor
COPY . ${APP_HOME}

# Crear directorio de uploads con permisos apropiados
RUN mkdir -p ${APP_HOME}/uploads/avatars && \
    chown -R appuser:appuser ${APP_HOME}

# Cambiar al usuario no-root
USER appuser

# Exponer el puerto 8001 (puerto estándar del microservicio)
# Este puerto es donde escuchará la aplicación FastAPI
EXPOSE 8001

# Healthcheck para monitorear la salud del contenedor
# Verifica cada 30 segundos si la aplicación está respondiendo
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8001/').read()" || exit 1

# Comando de inicio: ejecutar la aplicación con uvicorn
# --host 0.0.0.0: Escucha en todas las interfaces de red (necesario en Docker)
# --port 8001: Puerto expuesto
# --workers 2: Número de procesos worker (ajusta según tus necesidades)
# app.main:app: Importa la aplicación FastAPI desde app/main.py
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001", "--workers", "2"]