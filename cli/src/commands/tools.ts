import { readFile, writeFile, mkdir, access } from 'node:fs/promises';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import chalk from 'chalk';
import { logger } from '../utils/logger.js';

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
 * Options for gitignore updater
 */
export interface GitignoreOptions {
    force?: boolean;
    silent?: boolean;
    cwd?: string;
}

/**
 * Append or update .gitignore to ignore Flutter Pro Max internal files
 */
export async function updateGitignore(options: GitignoreOptions = {}): Promise<boolean> {
    const cwd = options.cwd || process.cwd();
    const gitignorePath = join(cwd, '.gitignore');
    const templatePath = join(ASSETS_DIR, 'templates', 'tools', 'gitignore.template');

    try {
        const templateContent = await readFile(templatePath, 'utf-8');
        const marker = '# Flutter Pro Max — AI Skill & Design System Artifacts';

        let existingContent = '';
        const exists = await fileExists(gitignorePath);
        if (exists) {
            existingContent = await readFile(gitignorePath, 'utf-8');
        }

        if (existingContent.includes(marker) && !options.force) {
            if (!options.silent) {
                logger.info('.gitignore already includes Flutter Pro Max rules. Skipping.');
            }
            return false;
        }

        let newContent = '';
        if (!exists || existingContent.trim().length === 0) {
            newContent = templateContent.trim() + '\n';
        } else {
            // If existing contains trailing newlines
            const separator = existingContent.endsWith('\n\n') ? '' : existingContent.endsWith('\n') ? '\n' : '\n\n';
            newContent = existingContent + separator + templateContent.trim() + '\n';
        }

        await writeFile(gitignorePath, newContent, 'utf-8');
        if (!options.silent) {
            logger.success(`Updated ${chalk.bold('.gitignore')} to ignore Flutter Pro Max internal assets.`);
        }
        return true;
    } catch (err) {
        if (!options.silent) {
            logger.error(`Failed to update .gitignore: ${err instanceof Error ? err.message : String(err)}`);
        }
        return false;
    }
}
