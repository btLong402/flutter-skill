import { readFile, writeFile, mkdir, access } from 'node:fs/promises';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import chalk from 'chalk';
import { logger } from '../utils/logger.js';
import { detectAIType } from '../utils/detect.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const ASSETS_DIR = join(__dirname, '..', '..', 'assets');

async function fileExists(path: string): Promise<boolean> {
    try {
        await access(path);
        return true;
    } catch {
        return false;
    }
}

/**
 * Options for Makefile generation
 */
export interface MakefileOptions {
    force?: boolean;
    cwd?: string;
}

/**
 * Generate a professional Makefile for Flutter projects
 */
export async function generateMakefile(options: MakefileOptions = {}): Promise<boolean> {
    const cwd = options.cwd || process.cwd();
    const targetFile = join(cwd, 'Makefile');
    const templateFile = join(ASSETS_DIR, 'templates', 'tools', 'Makefile.template');

    if (await fileExists(targetFile) && !options.force) {
        logger.warn('Makefile already exists in this directory. Use --force (-f) to overwrite.');
        return false;
    }

    try {
        const content = await readFile(templateFile, 'utf-8');
        await writeFile(targetFile, content, 'utf-8');
        logger.success(`Created ${chalk.bold('Makefile')} with professional Flutter workflows.`);
        console.log(chalk.dim('  Run `make help` to inspect available build, test, and code gen targets.'));
        return true;
    } catch (err) {
        logger.error(`Failed to generate Makefile: ${err instanceof Error ? err.message : String(err)}`);
        return false;
    }
}

/**
 * Options for Fastlane generation
 */
export interface FastlaneOptions {
    force?: boolean;
    platform?: 'android' | 'ios' | 'all';
    cwd?: string;
}

/**
 * Generate professional Fastlane setup for Android and iOS in Flutter
 */
export async function generateFastlane(options: FastlaneOptions = {}): Promise<boolean> {
    const cwd = options.cwd || process.cwd();
    const platform = options.platform || 'all';
    const templatesDir = join(ASSETS_DIR, 'templates', 'tools', 'fastlane');

    let createdAny = false;

    // 1. Android Fastlane
    if (platform === 'android' || platform === 'all') {
        const androidDir = join(cwd, 'android');
        const hasAndroid = await fileExists(androidDir);

        if (hasAndroid || platform === 'android') {
            const fastlaneDir = join(androidDir, 'fastlane');
            await mkdir(fastlaneDir, { recursive: true });

            const files = ['Appfile', 'Fastfile'];
            for (const file of files) {
                const targetPath = join(fastlaneDir, file);
                if (await fileExists(targetPath) && !options.force) {
                    logger.warn(`android/fastlane/${file} already exists. Skipping (use -f to overwrite).`);
                } else {
                    const src = join(templatesDir, 'android', file);
                    const content = await readFile(src, 'utf-8');
                    await writeFile(targetPath, content, 'utf-8');
                    createdAny = true;
                    logger.success(`Generated ${chalk.cyan(`android/fastlane/${file}`)}`);
                }
            }
        }
    }

    // 2. iOS Fastlane
    if (platform === 'ios' || platform === 'all') {
        const iosDir = join(cwd, 'ios');
        const hasIos = await fileExists(iosDir);

        if (hasIos || platform === 'ios') {
            const fastlaneDir = join(iosDir, 'fastlane');
            await mkdir(fastlaneDir, { recursive: true });

            const files = ['Appfile', 'Fastfile'];
            for (const file of files) {
                const targetPath = join(fastlaneDir, file);
                if (await fileExists(targetPath) && !options.force) {
                    logger.warn(`ios/fastlane/${file} already exists. Skipping (use -f to overwrite).`);
                } else {
                    const src = join(templatesDir, 'ios', file);
                    const content = await readFile(src, 'utf-8');
                    await writeFile(targetPath, content, 'utf-8');
                    createdAny = true;
                    logger.success(`Generated ${chalk.cyan(`ios/fastlane/${file}`)}`);
                }
            }
        }
    }

    // 3. Fastlane Environment Example
    const envExampleTarget = join(cwd, '.env.fastlane.example');
    if (!await fileExists(envExampleTarget) || options.force) {
        try {
            const envContent = await readFile(join(templatesDir, 'env.example'), 'utf-8');
            await writeFile(envExampleTarget, envContent, 'utf-8');
            logger.success(`Generated environment template ${chalk.cyan('.env.fastlane.example')}`);
            console.log(chalk.dim('  Copy to `.env.fastlane` and fill in credentials (do NOT commit .env.fastlane!).'));
            createdAny = true;
        } catch {
            // Ignore if template missing
        }
    }

    return createdAny;
}

/**
 * Mapping of AI assistant types to their generated folders/rules in projects
 */
export const AI_GITIGNORE_MAP: Record<string, { name: string; entries: string[] }> = {
    antigravity: {
        name: 'Antigravity / Generic Agent',
        entries: ['.agents/'],
    },
    claude: {
        name: 'Claude Code',
        entries: [
            '.claude/skills/flutter-pro-max/',
            '.claude/agents/flutter-design-review.md',
            '.claude/commands/flutter-review.md',
        ],
    },
    cursor: {
        name: 'Cursor',
        entries: ['.cursor/rules/', '.cursor/commands/'],
    },
    windsurf: {
        name: 'Windsurf',
        entries: ['.windsurf/rules/', '.windsurf/skills/'],
    },
    copilot: {
        name: 'GitHub Copilot',
        entries: [
            '.github/skills/flutter-pro-max/',
            '.github/copilot-instructions.md',
        ],
    },
    gemini: {
        name: 'Gemini Code Assist',
        entries: ['.gemini/'],
    },
    trae: {
        name: 'Trae',
        entries: ['.trae/'],
    },
    roocode: {
        name: 'Roo Code',
        entries: ['.roo/rules/', '.roo/commands/'],
    },
    kiro: {
        name: 'Kiro',
        entries: ['.kiro/rules/', '.kiro/steering/'],
    },
    continue: {
        name: 'Continue',
        entries: ['.continue/'],
    },
    codebuddy: {
        name: 'CodeBuddy',
        entries: ['.codebuddy/'],
    },
    codex: {
        name: 'Codex',
        entries: ['.codex/'],
    },
    junie: {
        name: 'Junie',
        entries: ['.junie/'],
    },
    opencode: {
        name: 'OpenCode',
        entries: ['.opencode/'],
    },
    qoder: {
        name: 'Qoder',
        entries: ['.qoder/'],
    },
    vscode: {
        name: 'VS Code',
        entries: ['.vscode/rules/', '.github/skills/flutter-pro-max/'],
    },
};

/**
 * Base artifacts that every Flutter Pro Max install creates
 */
export const BASE_GITIGNORE_ENTRIES = [
    '.shared/',
    'design-system/pages/',
    '__pycache__/',
    '*.py[cod]',
    '*$py.class',
    '.pytest_cache/',
    'coverage/',
    '*.lcov',
    '.fvm/flutter_sdk',
];

/**
 * Options for gitignore updater
 */
export interface GitignoreOptions {
    ai?: string;
    all?: boolean;
    force?: boolean;
    silent?: boolean;
    cwd?: string;
}

/**
 * Append or update .gitignore to ignore Flutter Pro Max internal files and specific AI assistant outputs
 */
export async function updateGitignore(options: GitignoreOptions = {}): Promise<boolean> {
    const cwd = options.cwd || process.cwd();
    const gitignorePath = join(cwd, '.gitignore');

    try {
        let existingContent = '';
        const exists = await fileExists(gitignorePath);
        if (exists) {
            existingContent = await readFile(gitignorePath, 'utf-8');
        }

        const linesToAppend: string[] = [];
        const hasHeader = existingContent.includes('# Flutter Pro Max — AI Skill & Design System Artifacts');

        // 1. If base header doesn't exist, add full header and base artifacts
        if (!hasHeader) {
            linesToAppend.push('# ==============================================================================');
            linesToAppend.push('# Flutter Pro Max — AI Skill & Design System Artifacts');
            linesToAppend.push('# ==============================================================================');
            for (const baseEntry of BASE_GITIGNORE_ENTRIES) {
                if (!existingContent.includes(baseEntry)) {
                    linesToAppend.push(baseEntry);
                }
            }
        } else {
            // Check if any base entry is missing
            for (const baseEntry of BASE_GITIGNORE_ENTRIES) {
                if (!existingContent.includes(baseEntry)) {
                    linesToAppend.push(baseEntry);
                }
            }
        }

        // 2. Determine which AI assistants to include
        const targetAIs: string[] = [];

        if (options.all || options.ai === 'all') {
            targetAIs.push(...Object.keys(AI_GITIGNORE_MAP));
        } else if (options.ai && AI_GITIGNORE_MAP[options.ai]) {
            targetAIs.push(options.ai);
        } else {
            // Auto-detect which AI directories exist in project
            const { detected } = detectAIType(cwd);
            if (detected.length > 0) {
                for (const d of detected) {
                    if (AI_GITIGNORE_MAP[d]) {
                        targetAIs.push(d);
                    }
                }
            }
            // Check if .agents folder exists directly
            if (await fileExists(join(cwd, '.agents')) && !targetAIs.includes('antigravity')) {
                targetAIs.push('antigravity');
            }
            // If still empty and no specific AI was given, include all common platforms
            if (targetAIs.length === 0) {
                targetAIs.push('antigravity', 'claude', 'cursor', 'windsurf', 'copilot');
            }
        }

        // 3. Add AI-specific ignore entries
        for (const ai of targetAIs) {
            const info = AI_GITIGNORE_MAP[ai];
            if (!info) continue;

            const missingEntries = info.entries.filter(e => !existingContent.includes(e));
            if (missingEntries.length > 0 || options.force) {
                linesToAppend.push('');
                linesToAppend.push(`# ${info.name}`);
                for (const entry of (options.force ? info.entries : missingEntries)) {
                    linesToAppend.push(entry);
                }
            }
        }

        // If nothing needs to be added and not forced
        if (linesToAppend.length === 0 && !options.force) {
            if (!options.silent) {
                logger.info('.gitignore is already up-to-date with Flutter Pro Max rules. Skipping.');
            }
            return false;
        }

        // 4. Write back to .gitignore
        let newContent = '';
        if (!exists || existingContent.trim().length === 0) {
            newContent = linesToAppend.join('\n') + '\n';
        } else {
            const separator = existingContent.endsWith('\n\n') ? '' : existingContent.endsWith('\n') ? '\n' : '\n\n';
            newContent = existingContent + separator + linesToAppend.join('\n') + '\n';
        }

        await writeFile(gitignorePath, newContent, 'utf-8');
        if (!options.silent) {
            logger.success(`Updated ${chalk.bold('.gitignore')} with AI-specific ignore rules for: ${chalk.cyan(targetAIs.join(', '))}`);
        }
        return true;
    } catch (err) {
        if (!options.silent) {
            logger.error(`Failed to update .gitignore: ${err instanceof Error ? err.message : String(err)}`);
        }
        return false;
    }
}
