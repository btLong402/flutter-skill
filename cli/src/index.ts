#!/usr/bin/env node

import { Command } from 'commander';
import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import { initCommand } from './commands/init.js';
import { versionsCommand } from './commands/versions.js';
import { updateCommand } from './commands/update.js';
import { generateMakefile, generateFastlane, updateGitignore } from './commands/tools.js';
import type { AIType } from './types/index.js';
import { AI_TYPES } from './types/index.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const pkg = JSON.parse(readFileSync(join(__dirname, '../package.json'), 'utf-8'));

const program = new Command();

program
    .name('flutter-pro-max')
    .description('CLI to install Flutter Pro Max skill for AI coding assistants')
    .version(pkg.version);

program
    .command('init')
    .description('Install Flutter Pro Max skill to current project')
    .option('-a, --ai <type>', `AI assistant type (${AI_TYPES.join(', ')})`)
    .option('-f, --force', 'Overwrite existing files')
    .option('--skip-gitignore', 'Skip automatic .gitignore configuration')
    .action(async (options) => {
        if (options.ai && !AI_TYPES.includes(options.ai)) {
            console.error(`Invalid AI type: ${options.ai}`);
            console.error(`Valid types: ${AI_TYPES.join(', ')}`);
            process.exit(1);
        }
        await initCommand({
            ai: options.ai as AIType | undefined,
            force: options.force,
            skipGitignore: options.skipGitignore,
        });
    });

program
    .command('makefile')
    .description('Generate professional Makefile with Flutter build, test, and code-gen workflows')
    .option('-f, --force', 'Overwrite existing Makefile if present')
    .action(async (options) => {
        await generateMakefile({ force: options.force });
    });

program
    .command('fastlane')
    .description('Generate professional Fastlane CI/CD automation for Android and iOS')
    .option('-f, --force', 'Overwrite existing Fastlane files if present')
    .option('-p, --platform <platform>', 'Target platform (android, ios, all)', 'all')
    .action(async (options) => {
        await generateFastlane({
            force: options.force,
            platform: options.platform as 'android' | 'ios' | 'all',
        });
    });

program
    .command('gitignore')
    .description('Configure .gitignore to exclude Flutter Pro Max internal skill assets and AI assistant folders')
    .option('-a, --ai <type>', 'Target AI assistant type (e.g., antigravity, claude, cursor, all)')
    .option('--all', 'Include ignore patterns for all supported AI assistants')
    .option('-f, --force', 'Force re-adding the ignore rules block')
    .action(async (options) => {
        await updateGitignore({
            ai: options.ai,
            all: options.all,
            force: options.force,
        });
    });

// Tools subcommand group
const toolsGroup = program
    .command('tools')
    .description('Developer utility generators (makefile, fastlane, gitignore)');

toolsGroup
    .command('makefile')
    .description('Generate professional Makefile')
    .option('-f, --force', 'Overwrite existing Makefile')
    .action(async (options) => {
        await generateMakefile({ force: options.force });
    });

toolsGroup
    .command('fastlane')
    .description('Generate professional Fastlane CI/CD setup')
    .option('-f, --force', 'Overwrite existing Fastlane files')
    .option('-p, --platform <platform>', 'Target platform (android, ios, all)', 'all')
    .action(async (options) => {
        await generateFastlane({
            force: options.force,
            platform: options.platform as 'android' | 'ios' | 'all',
        });
    });

toolsGroup
    .command('gitignore')
    .description('Configure .gitignore to exclude skill assets and AI assistant folders')
    .option('-a, --ai <type>', 'Target AI assistant type (e.g., antigravity, claude, cursor, all)')
    .option('--all', 'Include ignore patterns for all supported AI assistants')
    .option('-f, --force', 'Force update .gitignore')
    .action(async (options) => {
        await updateGitignore({
            ai: options.ai,
            all: options.all,
            force: options.force,
        });
    });

program
    .command('versions')
    .description('List available versions')
    .action(versionsCommand);

program
    .command('update')
    .description('Update Flutter Pro Max to latest version')
    .option('-a, --ai <type>', `AI assistant type (${AI_TYPES.join(', ')})`)
    .action(async (options) => {
        if (options.ai && !AI_TYPES.includes(options.ai)) {
            console.error(`Invalid AI type: ${options.ai}`);
            console.error(`Valid types: ${AI_TYPES.join(', ')}`);
            process.exit(1);
        }
        await updateCommand({
            ai: options.ai as AIType | undefined,
        });
    });

// Default command (when run without subcommand)
program
    .action(async () => {
        await initCommand({});
    });

program.parse();
