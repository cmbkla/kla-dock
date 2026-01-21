"""
HTML/CSS/JS template for KLA Dock web interface
"""

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>KLA Dock</title>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        :root {
            --bg-primary: #0a0e14;
            --bg-secondary: #151a23;
            --bg-card: #1a1f2e;
            --accent-cyan: #00d4ff;
            --accent-green: #00ff88;
            --accent-orange: #ff6b35;
            --accent-red: #ff3864;
            --text-primary: #e6edf3;
            --text-secondary: #8b949e;
            --border: #30363d;
        }
        
        body {
            font-family: 'JetBrains Mono', monospace;
            background: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.6;
            overflow-x: hidden;
        }
        
        /* Animated background */
        body::before {
            content: '';
            position: fixed;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: 
                radial-gradient(circle at 20% 50%, rgba(0, 212, 255, 0.03) 0%, transparent 50%),
                radial-gradient(circle at 80% 80%, rgba(0, 255, 136, 0.03) 0%, transparent 50%),
                radial-gradient(circle at 40% 20%, rgba(255, 107, 53, 0.02) 0%, transparent 50%);
            animation: drift 30s ease-in-out infinite;
            z-index: 0;
        }
        
        @keyframes drift {
            0%, 100% { transform: translate(0, 0) rotate(0deg); }
            33% { transform: translate(3%, 3%) rotate(1deg); }
            66% { transform: translate(-3%, 2%) rotate(-1deg); }
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 2rem;
            position: relative;
            z-index: 1;
        }
        
        header {
            margin-bottom: 3rem;
            border-bottom: 2px solid var(--border);
            padding-bottom: 2rem;
        }
        
        h1 {
            font-family: 'Space Mono', monospace;
            font-size: 2.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, var(--accent-cyan), var(--accent-green));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 0.5rem;
            letter-spacing: -0.02em;
            animation: slideDown 0.6s ease-out;
        }
        
        @keyframes slideDown {
            from {
                opacity: 0;
                transform: translateY(-20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .status-bar {
            display: flex;
            gap: 2rem;
            font-size: 0.9rem;
            color: var(--text-secondary);
            animation: fadeIn 0.8s ease-out 0.2s both;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        .status-item {
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .status-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: var(--accent-green);
            animation: pulse 2s ease-in-out infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.4; }
        }
        
        .section {
            margin-bottom: 3rem;
            animation: slideUp 0.6s ease-out both;
        }
        
        .section:nth-child(2) { animation-delay: 0.1s; }
        .section:nth-child(3) { animation-delay: 0.2s; }
        
        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        h2 {
            font-family: 'Space Mono', monospace;
            font-size: 1.5rem;
            margin-bottom: 1.5rem;
            color: var(--accent-cyan);
            display: flex;
            align-items: center;
            gap: 0.5rem;
            cursor: pointer;
            user-select: none;
            transition: color 0.2s ease;
        }
        
        h2:hover {
            color: var(--accent-green);
        }
        
        h2::before {
            content: '▼';
            color: var(--accent-green);
            transition: transform 0.3s ease;
            display: inline-block;
        }
        
        h2.collapsed::before {
            transform: rotate(-90deg);
        }
        
        .section-content {
            max-height: 10000px;
            overflow: visible;
            transition: max-height 0.3s ease, opacity 0.3s ease;
            padding-bottom: 1rem;
        }
        
        .section-content.collapsed {
            max-height: 0;
            opacity: 0;
            padding-bottom: 0;
        }
        
        .cards {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 1.5rem;
        }
        
        .card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 1.5rem;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }
        
        .card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 3px;
            background: linear-gradient(90deg, var(--accent-cyan), var(--accent-green));
            transform: scaleX(0);
            transform-origin: left;
            transition: transform 0.3s ease;
        }
        
        .card:hover {
            border-color: var(--accent-cyan);
            transform: translateY(-4px);
            box-shadow: 0 12px 24px rgba(0, 212, 255, 0.15);
        }
        
        .card:hover::before {
            transform: scaleX(1);
        }
        
        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: start;
            margin-bottom: 1rem;
        }
        
        .card-title {
            font-weight: 600;
            font-size: 1.1rem;
            color: var(--text-primary);
            word-break: break-word;
        }
        
        .badge {
            padding: 0.25rem 0.75rem;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .badge.running {
            background: rgba(0, 255, 136, 0.15);
            color: var(--accent-green);
            border: 1px solid var(--accent-green);
        }
        
        .badge.exited {
            background: rgba(139, 148, 158, 0.15);
            color: var(--text-secondary);
            border: 1px solid var(--border);
        }
        
        .card-info {
            font-size: 0.85rem;
            color: var(--text-secondary);
            margin-bottom: 1rem;
            line-height: 1.8;
        }
        
        .card-info div {
            display: flex;
            justify-content: space-between;
            padding: 0.25rem 0;
        }
        
        .card-info .label {
            color: var(--text-secondary);
        }
        
        .card-info .value {
            color: var(--text-primary);
            font-weight: 600;
        }
        
        .stats {
            margin: 1rem 0;
            padding: 1rem;
            background: var(--bg-secondary);
            border-radius: 6px;
            border: 1px solid var(--border);
        }
        
        .stat-row {
            display: flex;
            justify-content: space-between;
            margin-bottom: 0.5rem;
            font-size: 0.85rem;
        }
        
        .stat-row:last-child {
            margin-bottom: 0;
        }
        
        .progress-bar {
            height: 4px;
            background: var(--bg-secondary);
            border-radius: 2px;
            overflow: hidden;
            margin-top: 0.5rem;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, var(--accent-cyan), var(--accent-green));
            transition: width 0.5s ease;
        }
        
        .actions {
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
        }
        
        button {
            padding: 0.5rem 1rem;
            border: 1px solid var(--border);
            background: var(--bg-secondary);
            color: var(--text-primary);
            border-radius: 4px;
            cursor: pointer;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.85rem;
            font-weight: 600;
            transition: all 0.2s ease;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            position: relative;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        button:hover:not(:disabled) {
            background: var(--bg-card);
            border-color: var(--accent-cyan);
            color: var(--accent-cyan);
            transform: translateY(-1px);
        }
        
        button:active:not(:disabled) {
            transform: translateY(0);
        }
        
        button:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        
        button.danger:hover:not(:disabled) {
            border-color: var(--accent-red);
            color: var(--accent-red);
        }
        
        .btn-spinner {
            width: 12px;
            height: 12px;
            border: 2px solid var(--border);
            border-top-color: var(--accent-cyan);
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
        }
        
        .action-feedback {
            position: fixed;
            bottom: 2rem;
            right: 2rem;
            background: var(--bg-card);
            border: 1px solid var(--accent-green);
            color: var(--text-primary);
            padding: 1rem 1.5rem;
            border-radius: 8px;
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
            animation: slideInRight 0.3s ease-out;
            z-index: 1000;
        }
        
        .action-feedback.error {
            border-color: var(--accent-red);
        }
        
        @keyframes slideInRight {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        
        .empty-state {
            text-align: center;
            padding: 3rem;
            color: var(--text-secondary);
            font-size: 0.9rem;
            background: var(--bg-card);
            border: 1px dashed var(--border);
            border-radius: 8px;
        }
        
        .empty-state::before {
            content: '□';
            display: block;
            font-size: 3rem;
            margin-bottom: 1rem;
            opacity: 0.3;
        }
        
        .loading {
            display: inline-block;
            width: 12px;
            height: 12px;
            border: 2px solid var(--border);
            border-top-color: var(--accent-cyan);
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        
        .acr-status {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            padding: 1rem;
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 6px;
            margin-bottom: 1.5rem;
            font-size: 0.9rem;
        }
        
        .acr-status.authenticated {
            border-color: var(--accent-green);
        }
        
        .acr-status.error {
            border-color: var(--accent-red);
        }
        
        .acr-status-dot {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: var(--accent-green);
        }
        
        .acr-status.error .acr-status-dot {
            background: var(--accent-red);
        }
        
        .acr-search {
            width: 100%;
            padding: 0.75rem 1rem;
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            border-radius: 6px;
            color: var(--text-primary);
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.9rem;
            margin-bottom: 1.5rem;
            transition: border-color 0.2s ease;
        }
        
        .acr-search:focus {
            outline: none;
            border-color: var(--accent-cyan);
        }
        
        .acr-search::placeholder {
            color: var(--text-secondary);
        }
        
        .repo-card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            transition: all 0.3s ease;
        }
        
        .repo-card:hover {
            border-color: var(--accent-cyan);
            transform: translateX(4px);
        }
        
        .repo-name {
            font-weight: 600;
            font-size: 1.1rem;
            color: var(--text-primary);
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .repo-name::before {
            content: '📦';
        }
        
        .tag-list {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
        }
        
        .tag-item {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.5rem 1rem;
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            border-radius: 4px;
            font-size: 0.85rem;
        }
        
        .tag-item .tag-name {
            color: var(--text-secondary);
        }
        
        .tag-item button {
            padding: 0.25rem 0.75rem;
            font-size: 0.75rem;
        }
        
        /* Modal styles */
        .modal-overlay {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(10, 14, 20, 0.9);
            backdrop-filter: blur(4px);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 1000;
            animation: fadeIn 0.2s ease;
        }
        
        .modal {
            background: var(--bg-card);
            border: 1px solid var(--accent-cyan);
            border-radius: 8px;
            padding: 2rem;
            max-width: 500px;
            width: 90%;
            box-shadow: 0 20px 60px rgba(0, 212, 255, 0.3);
            animation: slideUp 0.3s ease;
        }
        
        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.5rem;
        }
        
        .modal-title {
            font-family: 'Space Mono', monospace;
            font-size: 1.3rem;
            color: var(--accent-cyan);
        }
        
        .modal-close {
            background: none;
            border: none;
            color: var(--text-secondary);
            font-size: 1.5rem;
            cursor: pointer;
            padding: 0;
            width: 30px;
            height: 30px;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: color 0.2s ease;
        }
        
        .modal-close:hover {
            color: var(--accent-red);
            transform: none;
        }
        
        .form-group {
            margin-bottom: 1.25rem;
        }
        
        .form-label {
            display: block;
            margin-bottom: 0.5rem;
            color: var(--text-secondary);
            font-size: 0.9rem;
            font-weight: 600;
        }
        
        .form-input {
            width: 100%;
            padding: 0.75rem 1rem;
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            border-radius: 6px;
            color: var(--text-primary);
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.95rem;
            transition: border-color 0.2s ease;
        }
        
        .form-input:focus {
            outline: none;
            border-color: var(--accent-cyan);
        }
        
        .form-input:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        
        .form-hint {
            font-size: 0.8rem;
            color: var(--text-secondary);
            margin-top: 0.25rem;
        }
        
        .saved-config-notice {
            text-align: center;
            font-size: 0.85rem;
            color: var(--text-secondary);
            margin-top: 1rem;
        }
        
        .saved-config-notice a {
            color: var(--accent-cyan);
            text-decoration: none;
            cursor: pointer;
        }
        
        .saved-config-notice a:hover {
            text-decoration: underline;
        }
        
        .modal-actions {
            display: flex;
            gap: 1rem;
            margin-top: 2rem;
        }
        
        .modal-actions button {
            flex: 1;
            padding: 0.75rem 1.5rem;
            font-size: 0.95rem;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, var(--accent-cyan), var(--accent-green));
            border-color: var(--accent-cyan);
            color: var(--bg-primary);
            font-weight: 700;
        }
        
        .btn-primary:hover:not(:disabled) {
            transform: translateY(-2px);
            box-shadow: 0 8px 16px rgba(0, 212, 255, 0.3);
        }
        
        .image-group {
            margin-bottom: 1.5rem;
        }
        
        .image-group-header {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            padding: 1rem 1.5rem;
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s ease;
            user-select: none;
        }
        
        .image-group-header:hover {
            border-color: var(--accent-cyan);
            transform: translateX(4px);
        }
        
        .image-group-header::before {
            content: '▼';
            color: var(--accent-green);
            transition: transform 0.3s ease;
            font-size: 0.8rem;
        }
        
        .image-group-header.collapsed::before {
            transform: rotate(-90deg);
        }
        
        .image-group-name {
            font-weight: 600;
            font-size: 1rem;
            color: var(--text-primary);
        }
        
        .image-group-name::before {
            content: '📦';
            margin-right: 0.5rem;
        }
        
        .image-group-count {
            color: var(--text-secondary);
            font-size: 0.85rem;
        }
        
        .image-group-tags {
            margin-top: 0.5rem;
            margin-left: 2rem;
            max-height: 1000px;
            overflow: hidden;
            transition: max-height 0.3s ease, opacity 0.3s ease;
        }
        
        .image-group-tags.collapsed {
            max-height: 0;
            opacity: 0;
        }
        
        .image-tag-card {
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 1rem 1.5rem;
            margin-bottom: 0.5rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: all 0.2s ease;
        }
        
        .image-tag-card:hover {
            border-color: var(--accent-cyan);
            transform: translateX(4px);
        }
        
        .image-tag-info {
            display: flex;
            gap: 1rem;
            align-items: center;
            flex: 1;
        }
        
        .image-tag-name {
            font-weight: 600;
            color: var(--text-primary);
        }
        
        .image-tag-size {
            color: var(--text-secondary);
            font-size: 0.85rem;
        }
        
        .image-tag-actions {
            display: flex;
            gap: 0.5rem;
        }
        
        .image-tag-actions button {
            padding: 0.5rem 1rem;
            font-size: 0.85rem;
        }
        
        .pull-status-card {
            background: var(--bg-card);
            border: 1px solid var(--accent-cyan);
            border-radius: 8px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            animation: slideDown 0.3s ease;
        }
        
        .pull-status-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
        }
        
        .pull-status-name {
            font-weight: 600;
            font-size: 1.1rem;
            color: var(--text-primary);
        }
        
        .pull-status-badge {
            padding: 0.25rem 0.75rem;
            background: rgba(0, 212, 255, 0.15);
            border: 1px solid var(--accent-cyan);
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: var(--accent-cyan);
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .pull-status-badge .loading {
            width: 10px;
            height: 10px;
        }
        
        .pull-progress-bar {
            background: var(--bg-secondary);
            border-radius: 4px;
            height: 8px;
            overflow: hidden;
            margin-bottom: 0.75rem;
        }
        
        .pull-progress-fill {
            height: 100%;
            background: linear-gradient(90deg, var(--accent-cyan), var(--accent-green));
            transition: width 0.5s ease;
            border-radius: 4px;
        }
        
        .pull-progress-text {
            display: flex;
            justify-content: space-between;
            font-size: 0.85rem;
            color: var(--text-secondary);
            margin-bottom: 0.5rem;
        }
        
        .pull-eta {
            color: var(--text-secondary);
            font-size: 0.85rem;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>⬢ KLA Dock</h1>
            <div class="status-bar">
                <div class="status-item">
                    <span class="status-dot"></span>
                    <span>Docker Connected</span>
                </div>
                <div class="status-item">
                    <span id="last-update">Last update: --</span>
                </div>
            </div>
        </header>
        
        <div class="section" id="active-pulls-section" style="display: none;">
            <h2 onclick="toggleSection('active-pulls')">Active Pulls</h2>
            <div class="section-content" id="active-pulls-section-content">
                <div id="active-pulls-list"></div>
            </div>
        </div>
        
        <div class="section">
            <h2 onclick="toggleSection('containers')">Containers</h2>
            <div class="section-content" id="containers-section">
                <div class="cards" id="containers"></div>
            </div>
        </div>
        
        <div class="section">
            <h2 onclick="toggleSection('images')">Images</h2>
            <div class="section-content" id="images-section">
                <div class="cards" id="images"></div>
            </div>
        </div>
        
        <div class="section">
            <h2 class="collapsed" onclick="toggleSection('registry')">Pull from Registry</h2>
            <div class="section-content collapsed" id="registry-section">
                <div class="acr-status" id="acr-status">
                    <span class="acr-status-dot"></span>
                    <span id="acr-status-text">Checking Azure CLI authentication...</span>
                </div>
                
                <div id="acr-selector-container">
                    <label for="acr-repo-select" style="display: block; margin-bottom: 0.5rem; color: var(--text-secondary); font-size: 0.9rem;">
                        Select your project:
                    </label>
                    <select 
                        id="acr-repo-select" 
                        class="acr-search"
                        style="cursor: pointer;"
                        onchange="selectRepository()"
                    >
                        <option value="">-- Choose a repository --</option>
                    </select>
                </div>
                
                <div id="acr-selected-repo" style="display: none;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                        <div>
                            <strong style="color: var(--accent-cyan);">Project:</strong> 
                            <span id="acr-current-repo" style="color: var(--text-primary);"></span>
                        </div>
                        <div style="display: flex; gap: 0.5rem;">
                            <button onclick="refreshTags()" style="padding: 0.5rem 1rem; font-size: 0.8rem;">
                                Refresh Tags
                            </button>
                            <button onclick="changeRepository()" style="padding: 0.5rem 1rem; font-size: 0.8rem;">
                                Change Project
                            </button>
                        </div>
                    </div>
                    
                    <div id="acr-tags-container"></div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Remove Container Confirmation Modal -->
    <div id="remove-container-modal" class="modal-overlay" style="display: none;" onclick="if(event.target === this) closeRemoveContainerModal()">
        <div class="modal" onclick="event.stopPropagation()">
            <div class="modal-header">
                <h3 class="modal-title">Remove Container</h3>
                <button class="modal-close" onclick="closeRemoveContainerModal()">×</button>
            </div>
            
            <div style="margin-bottom: 2rem;">
                <p style="color: var(--text-primary); margin-bottom: 1rem;">
                    Remove container <strong id="remove-container-name" style="color: var(--accent-red);"></strong>?
                </p>
                <p style="color: var(--text-secondary); font-size: 0.9rem;">
                    This action cannot be undone. The container will be permanently deleted.
                </p>
            </div>
            
            <div class="modal-actions">
                <button type="button" onclick="closeRemoveContainerModal()">Cancel</button>
                <button type="button" class="btn-primary danger" onclick="confirmRemoveContainer()">Remove Container</button>
            </div>
        </div>
    </div>
    
    <!-- Remove Image Confirmation Modal -->
    <div id="remove-image-modal" class="modal-overlay" style="display: none;" onclick="if(event.target === this) closeRemoveImageModal()">
        <div class="modal" onclick="event.stopPropagation()">
            <div class="modal-header">
                <h3 class="modal-title">Remove Image</h3>
                <button class="modal-close" onclick="closeRemoveImageModal()">×</button>
            </div>
            
            <div style="margin-bottom: 2rem;">
                <p style="color: var(--text-primary); margin-bottom: 1rem;">
                    Remove image <strong id="remove-image-name" style="color: var(--accent-red);"></strong>?
                </p>
                <p style="color: var(--text-secondary); font-size: 0.9rem;">
                    This action cannot be undone. The image will be permanently deleted.
                </p>
            </div>
            
            <div class="modal-actions">
                <button type="button" onclick="closeRemoveImageModal()">Cancel</button>
                <button type="button" class="btn-primary danger" onclick="confirmRemoveImage()">Remove Image</button>
            </div>
        </div>
    </div>
    
    <!-- Pull Confirmation Modal -->
    <div id="pull-confirm-modal" class="modal-overlay" style="display: none;" onclick="if(event.target === this) closePullConfirmModal()">
        <div class="modal" onclick="event.stopPropagation()">
            <div class="modal-header">
                <h3 class="modal-title">Pull Image from Registry</h3>
                <button class="modal-close" onclick="closePullConfirmModal()">×</button>
            </div>
            
            <div style="margin-bottom: 2rem;">
                <p style="color: var(--text-primary); margin-bottom: 1rem;">
                    Pull image <strong id="pull-confirm-image" style="color: var(--accent-cyan);"></strong>?
                </p>
                <p style="color: var(--text-secondary); font-size: 0.9rem;">
                    Large images may take several minutes to download. You can continue working while the pull completes in the background.
                </p>
            </div>
            
            <div class="modal-actions">
                <button type="button" onclick="closePullConfirmModal()">Cancel</button>
                <button type="button" class="btn-primary" onclick="confirmPullImage()">Pull Image</button>
            </div>
        </div>
    </div>
    
    <!-- Start Container Modal -->
    <div id="start-modal" class="modal-overlay" style="display: none;" onclick="if(event.target === this) closeStartModal()">
        <div class="modal" onclick="event.stopPropagation()">
            <div class="modal-header">
                <h3 class="modal-title">Start Container</h3>
                <button class="modal-close" onclick="closeStartModal()">×</button>
            </div>
            
            <form id="start-container-form" onsubmit="submitStartContainer(event)">
                <div class="form-group">
                    <label class="form-label">Container Name</label>
                    <input type="text" id="start-name" class="form-input" required />
                    <div class="form-hint">Name for this container instance</div>
                </div>
                
                <div class="form-group">
                    <label class="form-label">Host Port</label>
                    <input type="number" id="start-port" class="form-input" required min="1" max="65535" />
                    <div class="form-hint">Maps to container port 1433</div>
                </div>
                
                <div class="form-group">
                    <label class="form-label">SA Password</label>
                    <input type="password" id="start-password" class="form-input" required />
                    <div class="form-hint">SQL Server SA password</div>
                </div>
                
                <div id="saved-config-notice" class="saved-config-notice" style="display: none;">
                    Using saved config • <a onclick="enableConfigEdit()">edit</a>
                </div>
                
                <div class="modal-actions">
                    <button type="button" onclick="closeStartModal()">Cancel</button>
                    <button type="submit" class="btn-primary">Start Container</button>
                </div>
            </form>
        </div>
    </div>

    <script>
        const API_BASE = '';
        let actionInProgress = false;
        let acrData = { 
            repositories: [], 
            authenticated: false,
            selectedRepo: null,
            tags: []
        };
        let startModalData = null;
        let pullConfirmData = null;
        let removeContainerData = null;
        let removeImageData = null;
        let docker_state = {}; // Store latest state for pull button logic
        
        function openPullConfirmModal(repository, tag) {
            pullConfirmData = { repository, tag };
            document.getElementById('pull-confirm-image').textContent = `${repository}:${tag}`;
            document.getElementById('pull-confirm-modal').style.display = 'flex';
        }
        
        function closePullConfirmModal() {
            document.getElementById('pull-confirm-modal').style.display = 'none';
            pullConfirmData = null;
        }
        
        function confirmPullImage() {
            if (pullConfirmData) {
                pullImage(pullConfirmData.repository, pullConfirmData.tag);
                closePullConfirmModal();
            }
        }
        
        function openRemoveContainerModal(containerId, containerName) {
            removeContainerData = { id: containerId, name: containerName };
            document.getElementById('remove-container-name').textContent = containerName;
            document.getElementById('remove-container-modal').style.display = 'flex';
        }
        
        function closeRemoveContainerModal() {
            document.getElementById('remove-container-modal').style.display = 'none';
            removeContainerData = null;
        }
        
        function confirmRemoveContainer() {
            if (removeContainerData) {
                const btn = event.target;
                executeAction('remove', removeContainerData.id, 'container', btn);
                closeRemoveContainerModal();
            }
        }
        
        function openRemoveImageModal(imageId, imageName) {
            removeImageData = { id: imageId, name: imageName };
            document.getElementById('remove-image-name').textContent = imageName;
            document.getElementById('remove-image-modal').style.display = 'flex';
        }
        
        function closeRemoveImageModal() {
            document.getElementById('remove-image-modal').style.display = 'none';
            removeImageData = null;
        }
        
        function confirmRemoveImage() {
            if (removeImageData) {
                const btn = event.target;
                executeAction('remove', removeImageData.id, 'image', btn);
                closeRemoveImageModal();
            }
        }
        
        function renderActivePulls(pulls) {
            const section = document.getElementById('active-pulls-section');
            const container = document.getElementById('active-pulls-list');
            
            const pullKeys = Object.keys(pulls || {});
            
            if (pullKeys.length === 0) {
                section.style.display = 'none';
                return;
            }
            
            section.style.display = 'block';
            
            container.innerHTML = pullKeys.map(key => {
                const pull = pulls[key];
                const progress = pull.progress || 0;
                const elapsed = Date.now() - new Date(pull.started).getTime();
                const elapsedSec = Math.floor(elapsed / 1000);
                
                // Format elapsed time - always show seconds
                let elapsedStr = '';
                if (elapsedSec < 60) {
                    elapsedStr = `${elapsedSec}s`;
                } else {
                    const elapsedMin = Math.floor(elapsedSec / 60);
                    const remainingSec = elapsedSec % 60;
                    elapsedStr = `${elapsedMin}m ${remainingSec}s`;
                }
                
                let eta = '';
                if (progress > 5 && pull.total_bytes) {
                    const remainingBytes = pull.total_bytes - (pull.downloaded_bytes || 0);
                    const bytesPerMs = (pull.downloaded_bytes || 0) / elapsed;
                    const remainingMs = remainingBytes / bytesPerMs;
                    const remainingMin = Math.floor(remainingMs / 60000);
                    if (remainingMin > 0) {
                        eta = `~${remainingMin}m remaining`;
                    }
                }
                
                return `
                    <div class="pull-status-card">
                        <div class="pull-status-header">
                            <div class="pull-status-name">${key}</div>
                            <div class="pull-status-badge">
                                <span class="loading"></span>
                                Pulling
                            </div>
                        </div>
                        <div class="pull-progress-text">
                            <span>${progress.toFixed(1)}% complete</span>
                            <span>${pull.layers_complete || 0}/${pull.layers_total || '?'} layers</span>
                        </div>
                        <div class="pull-progress-bar">
                            <div class="pull-progress-fill" style="width: ${progress}%"></div>
                        </div>
                        <div class="pull-progress-text">
                            <span>Elapsed: ${elapsedStr}</span>
                            <span class="pull-eta">${eta}</span>
                        </div>
                    </div>
                `;
            }).join('');
        }
        
        function toggleSection(sectionId) {
            const header = event.currentTarget;
            const content = document.getElementById(`${sectionId}-section`);
            
            header.classList.toggle('collapsed');
            content.classList.toggle('collapsed');
        }
        
        function formatBytes(bytes) {
            if (!bytes || bytes === 'N/A') return 'N/A';
            const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
            if (bytes === 0) return '0 B';
            const i = Math.floor(Math.log(bytes) / Math.log(1024));
            return (bytes / Math.pow(1024, i)).toFixed(2) + ' ' + sizes[i];
        }
        
        function formatTime(timestamp) {
            const date = new Date(timestamp * 1000);
            return date.toLocaleString();
        }
        
        function getTimeSince(timestamp) {
            const now = Date.now() / 1000;
            const diff = now - timestamp;
            
            if (diff < 60) return 'Just now';
            if (diff < 3600) return Math.floor(diff / 60) + ' minutes ago';
            if (diff < 86400) return Math.floor(diff / 3600) + ' hours ago';
            return Math.floor(diff / 86400) + ' days ago';
        }
        
        function disableAllButtons(disabled) {
            const buttons = document.querySelectorAll('button');
            buttons.forEach(btn => btn.disabled = disabled);
        }
        
        function showFeedback(message, isError = false) {
            const existing = document.querySelector('.action-feedback');
            if (existing) existing.remove();
            
            const feedback = document.createElement('div');
            feedback.className = 'action-feedback' + (isError ? ' error' : '');
            feedback.textContent = message;
            document.body.appendChild(feedback);
            
            setTimeout(() => {
                feedback.style.opacity = '0';
                setTimeout(() => feedback.remove(), 300);
            }, 3000);
        }
        
        async function executeAction(action, target, type, buttonElement) {
            if (actionInProgress) return;
            actionInProgress = true;
            
            // Disable ALL buttons on the page
            disableAllButtons(true);
            
            // Show spinner on the clicked button
            const originalText = buttonElement.textContent;
            buttonElement.innerHTML = '<span class="btn-spinner"></span>' + originalText;
            
            try {
                const response = await fetch(`${API_BASE}/api/${action}`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ target, type })
                });
                const result = await response.json();
                
                if (result.success) {
                    showFeedback(`${action.charAt(0).toUpperCase() + action.slice(1)} successful`);
                    setTimeout(fetchData, 500); // Refresh after action
                } else {
                    showFeedback(`Error: ${result.error || 'Action failed'}`, true);
                }
                
                return result;
            } catch (error) {
                console.error('Action failed:', error);
                showFeedback(`Error: ${error.message}`, true);
                return { success: false, error: error.message };
            } finally {
                // Re-enable ALL buttons
                disableAllButtons(false);
                buttonElement.textContent = originalText;
                actionInProgress = false;
            }
        }
        
        function renderContainers(containers, stats) {
            const container = document.getElementById('containers');
            
            if (!containers || containers.length === 0) {
                container.innerHTML = '<div class="empty-state">No containers found</div>';
                return;
            }
            
            container.innerHTML = containers.map(c => {
                const stat = stats[c.id] || {};
                const isRunning = c.state === 'running';
                
                return `
                    <div class="card">
                        <div class="card-header">
                            <div class="card-title">${c.name}</div>
                            <span class="badge ${c.state}">${c.state}</span>
                        </div>
                        <div class="card-info">
                            <div><span class="label">Image:</span> <span class="value">${c.image}</span></div>
                            <div><span class="label">ID:</span> <span class="value">${c.id.substring(0, 12)}</span></div>
                            <div><span class="label">Created:</span> <span class="value">${getTimeSince(c.created)}</span></div>
                            ${c.ports ? `<div><span class="label">Ports:</span> <span class="value">${c.ports}</span></div>` : ''}
                        </div>
                        ${isRunning && stat.cpu ? `
                            <div class="stats">
                                <div class="stat-row">
                                    <span>CPU: ${stat.cpu}</span>
                                    <span>Memory: ${stat.memory}</span>
                                </div>
                                <div class="stat-row">
                                    <span>Net I/O: ${stat.net_io || 'N/A'}</span>
                                </div>
                            </div>
                        ` : ''}
                        <div class="actions">
                            ${isRunning ? 
                                `<button onclick="executeAction('stop', '${c.id}', 'container', this)">Stop</button>` :
                                `<button onclick="executeAction('start', '${c.id}', 'container', this)">Start</button>`
                            }
                            <button onclick="executeAction('restart', '${c.id}', 'container', this)">Restart</button>
                            <button class="danger" onclick="openRemoveContainerModal('${c.id}', '${c.name}')">Remove</button>
                        </div>
                    </div>
                `;
            }).join('');
        }
        
        function renderImages(images) {
            const container = document.getElementById('images');
            
            if (!images || images.length === 0) {
                container.innerHTML = '<div class="empty-state">No images found</div>';
                return;
            }
            
            // Group images by repository
            const grouped = {};
            images.forEach(img => {
                // Remove registry prefix if present
                let repo = img.repository;
                if (repo.includes('/')) {
                    repo = repo.split('/').pop();
                }
                
                if (!grouped[repo]) {
                    grouped[repo] = [];
                }
                grouped[repo].push(img);
            });
            
            // Render grouped images
            container.innerHTML = Object.keys(grouped).sort().map(repo => {
                const tags = grouped[repo];
                const groupId = `img-group-${repo.replace(/[^a-z0-9]/gi, '-')}`;
                
                return `
                    <div class="image-group">
                        <div class="image-group-header" onclick="toggleImageGroup('${groupId}')">
                            <span class="image-group-name">${repo}</span>
                            <span class="image-group-count">(${tags.length} tag${tags.length !== 1 ? 's' : ''})</span>
                        </div>
                        <div class="image-group-tags" id="${groupId}">
                            ${tags.map(img => {
                                const fullRepo = img.repository.includes('/') ? img.repository.split('/').pop() : img.repository;
                                return `
                                    <div class="image-tag-card">
                                        <div class="image-tag-info">
                                            <span class="image-tag-name">${img.tag}</span>
                                            <span class="image-tag-size">${formatBytes(img.size)}</span>
                                        </div>
                                        <div class="image-tag-actions">
                                            <button onclick="openStartModal('${fullRepo}', '${img.tag}', '${img.repository}')">Start</button>
                                            <button class="danger" onclick="openRemoveImageModal('${img.id}', '${img.repository}:${img.tag}')">Remove</button>
                                        </div>
                                    </div>
                                `;
                            }).join('')}
                        </div>
                    </div>
                `;
            }).join('');
        }
        
        function toggleImageGroup(groupId) {
            const group = document.getElementById(groupId);
            const header = event.currentTarget;
            
            header.classList.toggle('collapsed');
            group.classList.toggle('collapsed');
        }
        
        let acrInitialized = false;
        let currentSelectedRepo = null; // Track which repo is selected
        
        function renderACR(acrStatus) {
            // Track previous auth state
            const wasAuthenticated = acrData.authenticated;
            
            // Update status
            const statusEl = document.getElementById('acr-status');
            const statusTextEl = document.getElementById('acr-status-text');
            
            if (acrStatus.error) {
                statusEl.className = 'acr-status error';
                statusTextEl.textContent = `Error: ${acrStatus.error}`;
                acrInitialized = true;
                return;
            } else if (acrStatus.authenticated) {
                statusEl.className = 'acr-status authenticated';
                statusTextEl.textContent = 'Azure CLI authenticated';
            } else {
                statusEl.className = 'acr-status error';
                statusTextEl.textContent = 'Not authenticated - run: az login';
                acrInitialized = true;
                return;
            }
            
            // Store data globally
            acrData.authenticated = acrStatus.authenticated;
            acrData.repositories = acrStatus.repositories || [];
            
            // Only populate dropdown once
            if (!acrInitialized) {
                populateRepositoryDropdown();
                
                // Check if we have a saved selection
                const savedRepo = getSavedRepository();
                if (savedRepo && acrData.repositories.includes(savedRepo)) {
                    acrData.selectedRepo = savedRepo;
                    currentSelectedRepo = savedRepo;
                    loadRepositoryTags(savedRepo);
                }
                
                acrInitialized = true;
            } else if (!wasAuthenticated && acrStatus.authenticated) {
                // Auth status just changed from false to true - reload saved repo
                populateRepositoryDropdown();
                const savedRepo = getSavedRepository();
                if (savedRepo && acrData.repositories.includes(savedRepo)) {
                    acrData.selectedRepo = savedRepo;
                    currentSelectedRepo = savedRepo;
                    loadRepositoryTags(savedRepo);
                }
            } else if (currentSelectedRepo && acrData.tags.length > 0) {
                // Re-render tags to update pull button states
                renderTags(currentSelectedRepo, acrData.tags);
            }
        }
        
        function refreshTags() {
            if (acrData.selectedRepo) {
                loadRepositoryTags(acrData.selectedRepo);
            }
        }
        
        function getSavedRepository() {
            try {
                return localStorage.getItem('kla-dock-selected-repo');
            } catch (e) {
                return null;
            }
        }
        
        function saveRepository(repoName) {
            try {
                localStorage.setItem('kla-dock-selected-repo', repoName);
            } catch (e) {
                console.warn('Could not save repository selection');
            }
        }
        
        function populateRepositoryDropdown() {
            const select = document.getElementById('acr-repo-select');
            
            // Clear existing options except the first one
            select.innerHTML = '<option value="">-- Choose a repository --</option>';
            
            // Add repositories
            acrData.repositories.forEach(repo => {
                const option = document.createElement('option');
                option.value = repo;
                option.textContent = repo;
                if (repo === acrData.selectedRepo) {
                    option.selected = true;
                }
                select.appendChild(option);
            });
        }
        
        function selectRepository() {
            const select = document.getElementById('acr-repo-select');
            const repoName = select.value;
            
            if (!repoName) return;
            
            acrData.selectedRepo = repoName;
            saveRepository(repoName);
            loadRepositoryTags(repoName);
        }
        
        function changeRepository() {
            // Show dropdown, hide selected view
            document.getElementById('acr-selector-container').style.display = 'block';
            document.getElementById('acr-selected-repo').style.display = 'none';
            acrData.selectedRepo = null;
            currentSelectedRepo = null;
            
            // Clear tags immediately to avoid showing stale data
            acrData.tags = [];
        }
        
        async function loadRepositoryTags(repoName) {
            const tagsContainer = document.getElementById('acr-tags-container');
            tagsContainer.innerHTML = '<div style="text-align: center; padding: 2rem; color: var(--text-secondary);"><span class="loading"></span> Loading tags...</div>';
            
            // Show selected repository view
            document.getElementById('acr-selector-container').style.display = 'none';
            document.getElementById('acr-selected-repo').style.display = 'block';
            document.getElementById('acr-current-repo').textContent = repoName;
            
            // Store current selection
            currentSelectedRepo = repoName;
            
            try {
                const response = await fetch(`${API_BASE}/api/acr/tags?repository=${encodeURIComponent(repoName)}`);
                const result = await response.json();
                
                if (result.success) {
                    acrData.tags = result.tags;
                    renderTags(repoName, result.tags);
                } else {
                    tagsContainer.innerHTML = `<div class="empty-state">Error loading tags: ${result.error}</div>`;
                }
            } catch (error) {
                console.error('Failed to load tags:', error);
                tagsContainer.innerHTML = '<div class="empty-state">Failed to load tags</div>';
            }
        }
        
        function renderTags(repoName, tags) {
            const container = document.getElementById('acr-tags-container');
            
            if (!tags || tags.length === 0) {
                container.innerHTML = '<div class="empty-state">No tags found</div>';
                return;
            }
            
            // Get current images and active pulls to check status
            const existingImages = docker_state.images || [];
            const activePulls = docker_state.active_pulls || {};
            
            container.innerHTML = `
                <div style="margin-bottom: 1rem; color: var(--text-secondary); font-size: 0.9rem;">
                    ${tags.length} tag${tags.length !== 1 ? 's' : ''} available
                </div>
                <div class="tag-list" style="display: flex; flex-direction: column; gap: 0.5rem;">
                    ${tags.map(tag => {
                        const pullKey = `${repoName}:${tag}`;
                        const isPulling = pullKey in activePulls;
                        const imageExists = existingImages.some(img => {
                            const imgRepo = img.repository.includes('/') ? img.repository.split('/').pop() : img.repository;
                            return imgRepo === repoName && img.tag === tag;
                        });
                        
                        let buttonHtml = '';
                        if (isPulling) {
                            buttonHtml = '<button disabled>Pulling...</button>';
                        } else if (imageExists) {
                            buttonHtml = '<button disabled>Downloaded</button>';
                        } else {
                            buttonHtml = `<button onclick="openPullConfirmModal('${repoName}', '${tag}')">Pull</button>`;
                        }
                        
                        return `
                            <div class="tag-item" style="justify-content: space-between;">
                                <span class="tag-name" style="color: var(--text-primary); font-weight: 500;">${tag}</span>
                                ${buttonHtml}
                            </div>
                        `;
                    }).join('')}
                </div>
            `;
        }
        
        async function pullImage(repository, tag) {
            if (actionInProgress) return;
            actionInProgress = true;
            
            disableAllButtons(true);
            
            try {
                const response = await fetch(`${API_BASE}/api/acr/pull`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ repository, tag })
                });
                const result = await response.json();
                
                if (result.success) {
                    showFeedback(`Pull started for ${repository}:${tag}. Check Active Pulls section.`);
                    setTimeout(() => {
                        fetchData();
                    }, 500);
                } else {
                    showFeedback(`Error: ${result.error || 'Pull failed'}`, true);
                }
            } catch (error) {
                console.error('Pull failed:', error);
                showFeedback(`Error: ${error.message}`, true);
            } finally {
                disableAllButtons(false);
                actionInProgress = false;
            }
        }
        
        function openStartModal(repository, tag, fullImagePath) {
            startModalData = { repository, tag, fullImagePath };
            
            // Check for saved config
            const savedConfig = getContainerConfig(repository);
            const nameInput = document.getElementById('start-name');
            const portInput = document.getElementById('start-port');
            const passwordInput = document.getElementById('start-password');
            const notice = document.getElementById('saved-config-notice');
            
            if (savedConfig) {
                // Pre-fill with saved values
                nameInput.value = savedConfig.name;
                portInput.value = savedConfig.port;
                passwordInput.value = savedConfig.password;
                
                // Disable fields and show notice
                nameInput.disabled = true;
                portInput.disabled = true;
                passwordInput.disabled = true;
                notice.style.display = 'block';
            } else {
                // First time - suggest repository name
                nameInput.value = repository;
                portInput.value = '';
                passwordInput.value = '';
                
                nameInput.disabled = false;
                portInput.disabled = false;
                passwordInput.disabled = false;
                notice.style.display = 'none';
            }
            
            document.getElementById('start-modal').style.display = 'flex';
        }
        
        function closeStartModal() {
            document.getElementById('start-modal').style.display = 'none';
            startModalData = null;
        }
        
        function enableConfigEdit() {
            document.getElementById('start-name').disabled = false;
            document.getElementById('start-port').disabled = false;
            document.getElementById('start-password').disabled = false;
            document.getElementById('saved-config-notice').style.display = 'none';
        }
        
        function getContainerConfig(repository) {
            try {
                const key = `kla-dock-container-${repository}`;
                const saved = localStorage.getItem(key);
                return saved ? JSON.parse(saved) : null;
            } catch (e) {
                return null;
            }
        }
        
        function saveContainerConfig(repository, name, port, password) {
            try {
                const key = `kla-dock-container-${repository}`;
                localStorage.setItem(key, JSON.stringify({ name, port, password }));
            } catch (e) {
                console.warn('Could not save container config');
            }
        }
        
        async function submitStartContainer(event) {
            event.preventDefault();
            
            if (actionInProgress) return;
            actionInProgress = true;
            
            const name = document.getElementById('start-name').value;
            const port = document.getElementById('start-port').value;
            const password = document.getElementById('start-password').value;
            
            const submitBtn = event.target.querySelector('button[type="submit"]');
            const originalText = submitBtn.textContent;
            
            disableAllButtons(true);
            submitBtn.innerHTML = '<span class="btn-spinner"></span>Starting...';
            
            try {
                const response = await fetch(`${API_BASE}/api/container/start`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        image: startModalData.fullImagePath,
                        tag: startModalData.tag,
                        name: name,
                        port: port,
                        password: password
                    })
                });
                const result = await response.json();
                
                if (result.success) {
                    // Save config for next time
                    saveContainerConfig(startModalData.repository, name, port, password);
                    
                    showFeedback(`Container ${name} started successfully`);
                    closeStartModal();
                    setTimeout(() => {
                        fetchData();
                        // Scroll to containers section
                        document.getElementById('containers-section').scrollIntoView({ behavior: 'smooth' });
                    }, 500);
                } else {
                    showFeedback(`Error: ${result.error || 'Failed to start container'}`, true);
                }
            } catch (error) {
                console.error('Start failed:', error);
                showFeedback(`Error: ${error.message}`, true);
            } finally {
                disableAllButtons(false);
                submitBtn.textContent = originalText;
                actionInProgress = false;
            }
        }
        
        async function fetchData() {
            try {
                const response = await fetch(`${API_BASE}/api/status`);
                const data = await response.json();
                
                // Store globally for pull button logic
                docker_state = data;
                
                renderActivePulls(data.active_pulls);
                renderContainers(data.containers, data.stats);
                renderImages(data.images);
                renderACR({
                    authenticated: data.acr_authenticated,
                    repositories: data.acr_repositories,
                    error: data.acr_error
                });
                
                document.getElementById('last-update').textContent = 
                    `Last update: ${new Date().toLocaleTimeString()}`;
            } catch (error) {
                console.error('Failed to fetch data:', error);
            }
        }
        
        // Initial fetch and auto-refresh
        fetchData();
        setInterval(fetchData, 5000);
    </script>
</body>
</html>
'''