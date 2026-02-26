import { readFile, mkdir, writeFile, cp, access, readdir } from 'node:fs/promises';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import type { AIType, PlatformConfig } from '../types/index.js';

const __dirname = dirname(fileURLToPath(import.meta.url));
// After build: dist/utils/template.js -> ../../assets = cli/assets ✓
const ASSETS_DIR = join(__dirname, '..', '..', 'assets');

// Map AIType to platform config file name
const AI_TO_PLATFORM: Record<string, string> = {
    claude: 'claude',
    cursor: 'cursor',
    windsurf: 'windsurf',
    antigravity: 'agent',
    copilot: 'copilot',
    kiro: 'kiro',
    roocode: 'roocode',
    codex: 'codex',
    qoder: 'qoder',
    gemini: 'gemini',
    trae: 'trae',
    codebuddy: 'codebuddy',
    opencode: 'opencode',
    continue: 'continue',
    junie: 'junie',
    vscode: 'vscode',
};

async function exists(path: string): Promise<boolean> {
    try {
        await access(path);
        return true;
    } catch {
        return false;
    }
}

/**
 * Load platform configuration from JSON file
 */
export async function loadPlatformConfig(aiType: string): Promise<PlatformConfig> {
    const platformName = AI_TO_PLATFORM[aiType];
    if (!platformName) {
        throw new Error(`Unknown AI type: ${aiType}`);
    }

    const configPath = join(ASSETS_DIR, 'templates', 'platforms', `${platformName}.json`);
    const content = await readFile(configPath, 'utf-8');
    return JSON.parse(content) as PlatformConfig;
}

/**
 * Load all available platform configs
 */
export async function loadAllPlatformConfigs(): Promise<Map<string, PlatformConfig>> {
    const configs = new Map<string, PlatformConfig>();

    for (const [aiType, platformName] of Object.entries(AI_TO_PLATFORM)) {
        try {
            const config = await loadPlatformConfig(aiType);
            configs.set(aiType, config);
        } catch {
            // Skip if config doesn't exist
        }
    }

    return configs;
}

/**
 * Load a template file
 */
async function loadTemplate(templateName: string): Promise<string> {
    const templatePath = join(ASSETS_DIR, 'templates', templateName);
    return readFile(templatePath, 'utf-8');
}

/**
 * Render frontmatter section
 */
function renderFrontmatter(frontmatter: Record<string, string> | null): string {
    if (!frontmatter) return '';

    const lines = ['---'];
    for (const [key, value] of Object.entries(frontmatter)) {
        // Quote values that contain special characters
        if (value.includes(':') || value.includes('"') || value.includes('\n')) {
            lines.push(`${key}: "${value.replace(/"/g, '\\"')}"`);
        } else {
            lines.push(`${key}: ${value}`);
        }
    }
    lines.push('---', '');
    return lines.join('\n');
}

/**
 * Render skill file content from template
 */
export async function renderSkillFile(config: PlatformConfig): Promise<string> {
    // Load base template (use config.template or default to skill-content.md)
    const templateFile = config.template || 'skill-content.md';
    let content = await loadTemplate(`base/${templateFile}`);

    // Load quick reference if needed
    let quickReferenceContent = '';
    if (config.sections.quickReference) {
        quickReferenceContent = await loadTemplate('base/quick-reference.md');
        // Replace script path in quick reference
        quickReferenceContent = quickReferenceContent.replace(/\{\{SCRIPT_PATH\}\}/g, config.scriptPath);
    }

    // Build the final content
    const frontmatter = renderFrontmatter(config.frontmatter);

    // Replace placeholders
    const quickRefWithNewline = quickReferenceContent ? '\n' + quickReferenceContent : '';

    content = content
        .replace(/\{\{TITLE\}\}/g, config.title)
        .replace(/\{\{DESCRIPTION\}\}/g, config.description)
        .replace(/\{\{SCRIPT_PATH\}\}/g, config.scriptPath)
        .replace(/\{\{SKILL_OR_WORKFLOW\}\}/g, config.skillOrWorkflow)
        .replace(/\{\{QUICK_REFERENCE\}\}/g, quickRefWithNewline);

    return frontmatter + content;
}

/**
 * Copy data and scripts to target directory
 */
async function copyDataAndScripts(targetSkillDir: string): Promise<void> {
    const dataSource = join(ASSETS_DIR, 'data');
    const scriptsSource = join(ASSETS_DIR, 'scripts');

    const dataTarget = join(targetSkillDir, 'data');
    const scriptsTarget = join(targetSkillDir, 'scripts');

    // Copy data
    if (await exists(dataSource)) {
        await mkdir(dataTarget, { recursive: true });
        await cp(dataSource, dataTarget, { recursive: true });
    }

    // Copy scripts
    if (await exists(scriptsSource)) {
        await mkdir(scriptsTarget, { recursive: true });
        await cp(scriptsSource, scriptsTarget, { recursive: true });
    }
}

/**
 * Ensure .shared folder exists with data and scripts
 */
async function ensureSharedExists(targetDir: string): Promise<boolean> {
    const sharedDir = join(targetDir, '.shared', 'flutter-pro-max');

    // Check if already exists
    if (await exists(sharedDir)) {
        return false; // Already exists, didn't create
    }

    await mkdir(sharedDir, { recursive: true });
    await copyDataAndScripts(sharedDir);
    return true; // Created new
}

/**
 * Generate modular rules files for a platform
 */
async function generateRulesFile(
    targetDir: string,
    config: PlatformConfig
): Promise<void> {
    if (!config.rulesFile) return;

    // Load all rule files from templates/base/rules/
    const rulesDir = join(ASSETS_DIR, 'templates', 'base', 'rules');
    if (!await exists(rulesDir)) return;

    const ruleFiles = (await readdir(rulesDir))
        .filter(f => f.endsWith('.md'))
        .sort();

    if (ruleFiles.length === 0) return;

    if (config.rulesFile.mode === 'append') {
        // Append mode: concatenate all rules into target file (e.g. CLAUDE.md)
        const rulesFilePath = join(targetDir, config.rulesFile.path);
        const rulesFileDir = dirname(rulesFilePath);
        await mkdir(rulesFileDir, { recursive: true });

        let existing = '';
        if (await exists(rulesFilePath)) {
            existing = await readFile(rulesFilePath, 'utf-8');
            if (existing.includes('Flutter Pro Max — Agent Rules')) {
                return; // Already has rules
            }
            existing += '\n\n';
        }

        // Helper to strip YAML frontmatter for appended files
        const stripFrontmatter = (content: string) => {
            return content.replace(/^---\n[\s\S]*?\n---\n+/, '');
        };

        // Concatenate all rule files
        const allRules: string[] = ['# Flutter Pro Max — Agent Rules\n'];
        for (const file of ruleFiles) {
            const content = await readFile(join(rulesDir, file), 'utf-8');
            allRules.push(stripFrontmatter(content));
        }

        await writeFile(rulesFilePath, existing + allRules.join('\n---\n\n'), 'utf-8');
    } else {
        // Create mode: generate separate files in rules directory
        const rulesTargetDir = dirname(join(targetDir, config.rulesFile.path));
        await mkdir(rulesTargetDir, { recursive: true });

        // If rulesFile.path ends with .mdc, we use .mdc extension for files
        const useMdc = config.rulesFile.path.endsWith('.mdc');

        for (const file of ruleFiles) {
            const content = await readFile(join(rulesDir, file), 'utf-8');
            const targetExt = useMdc ? '.mdc' : '.md';
            const targetPath = join(rulesTargetDir, file.replace(/\.md$/, targetExt));
            
            await writeFile(targetPath, content, 'utf-8');
        }
    }
}

/**
 * Generate platform files for a specific AI type
 */
export async function generatePlatformFiles(
    targetDir: string,
    aiType: string
): Promise<string[]> {
    const config = await loadPlatformConfig(aiType);
    const createdFolders: string[] = [];

    // Determine full skill directory path
    const skillDir = join(
        targetDir,
        config.folderStructure.root,
        config.folderStructure.skillPath
    );

    // Create directory structure
    await mkdir(skillDir, { recursive: true });

    // Render and write skill file
    const skillContent = await renderSkillFile(config);
    const skillFilePath = join(skillDir, config.folderStructure.filename);
    await writeFile(skillFilePath, skillContent, 'utf-8');
    createdFolders.push(config.folderStructure.root);

    // Handle data/scripts based on install type
    if (config.installType === 'full') {
        // Full install: copy data and scripts into the skill directory
        await copyDataAndScripts(skillDir);
    } else {
        // Reference install: ensure .shared exists
        const createdShared = await ensureSharedExists(targetDir);
        if (createdShared) {
            createdFolders.push('.shared');
        }
    }

    // Generate rules file (standalone, separate from skill)
    await generateRulesFile(targetDir, config);

    return createdFolders;
}

/**
 * Generate files for all AI types
 */
export async function generateAllPlatformFiles(targetDir: string): Promise<string[]> {
    const allFolders = new Set<string>();

    for (const aiType of Object.keys(AI_TO_PLATFORM)) {
        try {
            const folders = await generatePlatformFiles(targetDir, aiType);
            folders.forEach(f => allFolders.add(f));
        } catch {
            // Skip if generation fails for a platform
        }
    }

    return Array.from(allFolders);
}

/**
 * Get list of supported AI types
 */
export function getSupportedAITypes(): string[] {
    return Object.keys(AI_TO_PLATFORM);
}
