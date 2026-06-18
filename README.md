# 🖥️ Hackathon Fase 5 - Frontend (Repo 5 de 5)

Este é o repositório final do Sistema de Processamento de Vídeos da FIAP X. Ele contém a interface gráfica de usuário (UI) desenvolvida em **Streamlit**, desenhada para fornecer uma experiência visual imersiva e responsiva.

## 🎯 Responsabilidades
- **Autenticação Visual:** Telas de Login e Registro de usuários que consomem a API Flask e gerenciam tokens JWT em memória.
- **Upload Simplificado:** Interface *Drag & Drop* para envio de arquivos de vídeo (`.mp4`, `.avi`, etc).
- **Acompanhamento de Status:** Dashboard listando os vídeos enviados pelo usuário com indicadores visuais de estado (`NA_FILA`, `PROCESSANDO`, `CONCLUIDO`, `ERRO`).
- **Download Direto:** Renderização de links diretos e seguros (AWS S3 Presigned URLs) para o download dos frames extraídos em `.zip`.

## 🛠️ Tecnologias Utilizadas
- **Python 3.11**
- **Streamlit:** Framework para criação rápida de Web Apps de dados.
- **Requests:** Para consumo das APIs HTTP.
- **Docker & Kubernetes (EKS):** Containerização e orquestração.
- **GitHub Actions:** Pipeline CI/CD.

## 🚀 Como Executar o Deploy
1. **Descubra a URL da API:** No cluster Kubernetes, obtenha o IP do LoadBalancer da API Flask (`kubectl get svc hackathon-api-lb`).
2. **Configuração de Secrets:** Vá no GitHub deste repositório e configure:
   - `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_SESSION_TOKEN`
   - `ECR_REPO` (URL do repositório ECR da API. Vamos reaproveitá-lo com a tag `frontend-latest`)
   - `API_URL` (Cole o endereço da API com `http://` no começo e sem barra no final).
3. Faça um push na branch `main`. A pipeline irá fazer o build da imagem Docker, enviá-la para o ECR e atualizar o cluster Kubernetes.

## 🌐 Acessando a Aplicação
Após o deploy, obtenha o IP público do Frontend executando:
```bash
kubectl get svc hackathon-frontend-lb