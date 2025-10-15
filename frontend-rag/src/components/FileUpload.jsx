import { memo, useCallback, useRef } from 'react';
// import { useRAGContext } from '../context/RAGContext';
// import { useRAG } from '../hooks/useRAG';

function FileUpload() {
  // TODO: Obter estados do Context

  const inputRef = useRef(null);

  // TODO: Implementar handleFileChange
  const handleFileChange = useCallback(async (e) => {

    console.log('File changed:', e.target.files?.[0]);
  }, []);

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
        className="upload-input"
      />

      {/* TODO: Mostrar informações do arquivo */}
      <div className="upload-info">
        <strong>Arquivo carregado:</strong>
        <br />
        <small>Páginas: | Chunks:</small>
      </div>
    </div>
  );
}

export default memo(FileUpload);
