import { memo, useCallback, useRef } from 'react';
import { useRAGContext } from '../context/RAGContext';
import { useRAG } from '../hooks/useRAG';

function FileUpload() {
  // TODO: Obter estados do Context
  const { uploadedFile, isLoading } = useRAGContext();
  const { uploadFile } = useRAG();

  const inputRef = useRef(null);

  // TODO: Implementar handleFileChange
  const handleFileChange = useCallback(async (e) => {
    const file = e.target.files?.[0];

    const result = await uploadFile(file);

    if (result.success) {
      alert(`Arquivo enviado: ${result.data.filename}`)
    } else {
      alert(`Erro ao enviar arquivo: ${result.error}`)
    }

    if (inputRef.current) {
      inputRef.current.value = '';
    }

    console.log('File changed:', e.target.files?.[0]);
  }, [uploadFile]);

  return (
    <div className="upload-container">
      <label htmlFor="file-upload" className="upload-label">
        📄 Fazer upload de PDF
      </label>

      <input
        ref={inputRef}
        id="file-upload"
        type="file"
        accept=".pdf"
        onChange={handleFileChange}
        disabled={isLoading}
        className="upload-input"
      />

      {/* TODO: Mostrar informações do arquivo */}
      {uploadedFile && (
        <div className="upload-info">

          <strong>Arquivo carregado:</strong> {uploadedFile.filename}
          <br />
          <small>Páginas: {uploadedFile.pages} | Chunks: {uploadedFile.chunks}</small> 
        </div>
      )}
    </div>
  );
}

export default memo(FileUpload);
