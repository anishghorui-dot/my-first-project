import React, { useState } from 'react';
import { Upload, FileText, CheckCircle, AlertCircle, Loader, Download, Search } from 'lucide-react';
import axios from 'axios';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [parsing, setParsing] = useState(false);
  const [fileId, setFileId] = useState(null);
  const [translations, setTranslations] = useState([]);
  const [metadata, setMetadata] = useState(null);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedTranslation, setSelectedTranslation] = useState(null);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      setError(null);
      setTranslations([]);
      setMetadata(null);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a file first');
      return;
    }

    setUploading(true);
    setError(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const uploadResponse = await axios.post('/api/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });

      const uploadedFileId = uploadResponse.data.file_id;
      setFileId(uploadedFileId);
      setUploading(false);

      // Now parse and translate
      setParsing(true);
      const parseResponse = await axios.get(`/api/parse/${uploadedFileId}`);
      
      setTranslations(parseResponse.data.translations);
      setMetadata(parseResponse.data.metadata);
      setParsing(false);

    } catch (err) {
      setError(err.response?.data?.error || 'Failed to process file');
      setUploading(false);
      setParsing(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile) {
      setFile(droppedFile);
      setError(null);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const filteredTranslations = translations.filter(t =>
    t.xpath.toLowerCase().includes(searchTerm.toLowerCase()) ||
    t.plain_language.toLowerCase().includes(searchTerm.toLowerCase()) ||
    t.activity.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const exportToMarkdown = () => {
    let markdown = `# TIBCO BW XPath Translation Report\n\n`;
    markdown += `**Process:** ${metadata?.process_name || 'Unknown'}\n\n`;
    markdown += `**Total XPath Expressions:** ${translations.length}\n\n`;
    markdown += `---\n\n`;

    translations.forEach((t, idx) => {
      markdown += `## Expression ${idx + 1}\n\n`;
      markdown += `**Location:** ${t.location} - ${t.activity}\n\n`;
      markdown += `**XPath:**\n\`\`\`xpath\n${t.xpath}\n\`\`\`\n\n`;
      markdown += `**Plain Language:** ${t.plain_language}\n\n`;
      
      if (t.steps && t.steps.length > 0) {
        markdown += `**Steps:**\n`;
        t.steps.forEach(step => {
          markdown += `- ${step}\n`;
        });
        markdown += `\n`;
      }
      
      markdown += `**Confidence:** ${t.confidence}\n\n`;
      markdown += `---\n\n`;
    });

    const blob = new Blob([markdown], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `xpath-translation-${Date.now()}.md`;
    a.click();
  };

  return (
    <div className="App">
      <header className="app-header">
        <div className="header-content">
          <FileText className="header-icon" size={32} />
          <div>
            <h1>TIBCO BW XPath Translator</h1>
            <p>Convert complex XPath expressions to plain language everyone can understand</p>
          </div>
        </div>
      </header>

      <main className="main-content">
        {!translations.length ? (
          <div className="upload-section">
            <div
              className={`drop-zone ${file ? 'has-file' : ''}`}
              onDrop={handleDrop}
              onDragOver={handleDragOver}
            >
              <Upload size={48} className="upload-icon" />
              <h2>Upload TIBCO BW Process File</h2>
              <p>Drag and drop your .xml, .process, or .bwp file here</p>
              
              <input
                type="file"
                id="file-input"
                accept=".xml,.process,.bwp"
                onChange={handleFileChange}
                style={{ display: 'none' }}
              />
              
              <label htmlFor="file-input" className="btn btn-primary">
                Choose File
              </label>

              {file && (
                <div className="file-info">
                  <FileText size={20} />
                  <span>{file.name}</span>
                  <span className="file-size">
                    ({(file.size / 1024).toFixed(2)} KB)
                  </span>
                </div>
              )}

              {error && (
                <div className="error-message">
                  <AlertCircle size={20} />
                  <span>{error}</span>
                </div>
              )}

              {file && !uploading && !parsing && (
                <button className="btn btn-success" onClick={handleUpload}>
                  Parse & Translate
                </button>
              )}

              {(uploading || parsing) && (
                <div className="loading-state">
                  <Loader className="spinner" size={24} />
                  <span>{uploading ? 'Uploading file...' : 'Parsing XPath expressions...'}</span>
                </div>
              )}
            </div>
          </div>
        ) : (
          <div className="results-section">
            <div className="results-header">
              <div className="results-info">
                <h2>{metadata?.process_name || 'Translation Results'}</h2>
                <p>{translations.length} XPath expressions found and translated</p>
              </div>
              
              <div className="results-actions">
                <button className="btn btn-secondary" onClick={exportToMarkdown}>
                  <Download size={18} />
                  Export Report
                </button>
                <button
                  className="btn btn-outline"
                  onClick={() => {
                    setFile(null);
                    setTranslations([]);
                    setMetadata(null);
                    setFileId(null);
                  }}
                >
                  Upload New File
                </button>
              </div>
            </div>

            <div className="search-bar">
              <Search size={20} />
              <input
                type="text"
                placeholder="Search by XPath, description, or activity..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>

            <div className="translations-grid">
              {filteredTranslations.map((translation, idx) => (
                <div
                  key={translation.id}
                  className={`translation-card ${selectedTranslation?.id === translation.id ? 'selected' : ''}`}
                  onClick={() => setSelectedTranslation(translation)}
                >
                  <div className="card-header">
                    <span className="card-number">#{idx + 1}</span>
                    <span className={`confidence-badge ${translation.confidence}`}>
                      {translation.confidence} confidence
                    </span>
                  </div>

                  <div className="card-location">
                    <strong>{translation.location}</strong>
                    {translation.activity && ` • ${translation.activity}`}
                  </div>

                  <div className="xpath-display">
                    <code>{translation.xpath}</code>
                  </div>

                  <div className="plain-language">
                    <CheckCircle size={16} className="check-icon" />
                    <p>{translation.plain_language}</p>
                  </div>

                  {translation.steps && translation.steps.length > 0 && (
                    <details className="steps-section">
                      <summary>View step-by-step breakdown</summary>
                      <ol>
                        {translation.steps.map((step, stepIdx) => (
                          <li key={stepIdx}>{step}</li>
                        ))}
                      </ol>
                    </details>
                  )}
                </div>
              ))}
            </div>

            {filteredTranslations.length === 0 && searchTerm && (
              <div className="no-results">
                <AlertCircle size={48} />
                <p>No translations match your search</p>
              </div>
            )}
          </div>
        )}
      </main>

      <footer className="app-footer">
        <p>TIBCO BW XPath Translator • Made for business users and developers</p>
      </footer>
    </div>
  );
}

export default App;
