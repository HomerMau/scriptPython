from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import subprocess as s

app = FastAPI()

class ArquivosModel(BaseModel):
    arquivos: List[str]

@app.post("/scriptRpa")
async def ler_arquivos_e_executar(dados: ArquivosModel):
    arquivos = dados.arquivos
    if not arquivos:
        raise HTTPException(status_code=400, detail="A lista de arquivos não pode estar vazia.")

    # Cria uma lista para armazenar a sequência e os arquivos
    arquivosLista = [{"seq": i + 1, "file": arquivo} for i, arquivo in enumerate(arquivos)]

    # Imprime a sequência dos arquivos
    print("\n\"files\": [")
    for arquivoDados in arquivosLista:
        print(f'  {{"seq": {arquivoDados["seq"]}, "file": "{arquivoDados["file"]}"}}'
              f'{"," if arquivoDados["seq"] < len(arquivosLista) else ""}')
    print("]")

    # Executa os scripts na ordem inserida
    for arquivo in arquivos:
        try:
            print(f"\nExecutando {arquivo}...")
            s.run(args=["python", arquivo], check=True)
        except s.CalledProcessError as e:
            raise HTTPException(status_code=500, detail=f"Erro ao executar o arquivo {arquivo}: {e}")
        except FileNotFoundError:
            raise HTTPException(status_code=404, detail=f"Arquivo não encontrado: {arquivo}")

    return {"message": "Scripts executados com sucesso", "files": arquivosLista}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
