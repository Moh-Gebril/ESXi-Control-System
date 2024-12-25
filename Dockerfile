# Stage 1: Build the Python application
FROM python:3.11-slim AS builder

# Set a working directory
WORKDIR /app

# Install system dependencies required by PyInstaller and Python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    openssh-client \
    && rm -rf /var/lib/apt/lists/*

# Install PyInstaller
RUN pip install --upgrade pip && pip install pyinstaller

# Copy the application files to the container
COPY . .

# Install application dependencies
RUN if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

# Create a standalone executable using PyInstaller
RUN pyinstaller --onefile /app/src/esxi_control_system.py

# Stage 2: Copy the executable to a clean image
FROM busybox:1.35-uclibc AS final

# Copy the executable from the builder stage
COPY --from=builder /app/dist/esxi_control_system /app/esxi_control_system

# Make the executable available for export
CMD ["cp", "/app/esxi_control_system", "/output/esxi_control_system"]
