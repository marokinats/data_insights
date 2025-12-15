const eslintConfigPrettier = require('eslint-config-prettier/flat');
const { defineConfig, globalIgnores } = require('eslint/config');

const globals = require('globals');

const { fixupConfigRules, fixupPluginRules } = require('@eslint/compat');

const tsParser = require('@typescript-eslint/parser');
const reactRefresh = require('eslint-plugin-react-refresh');
const typescriptEslint = require('@typescript-eslint/eslint-plugin');
const prettier = require('eslint-plugin-prettier');

const js = require('@eslint/js');

const { FlatCompat } = require('@eslint/eslintrc');

const compat = new FlatCompat({
  baseDirectory: __dirname,
  recommendedConfig: js.configs.recommended,
  allConfig: js.configs.all,
});

module.exports = defineConfig([
  {
    languageOptions: {
      globals: {
        ...globals.browser,
      },

      parser: tsParser,
      ecmaVersion: 'latest',
      sourceType: 'module',

      parserOptions: {
        ecmaFeatures: {
          jsx: true,
        },
      },
    },

    extends: fixupConfigRules(
      compat.extends(
        'eslint:recommended',
        'plugin:@typescript-eslint/recommended',
        'plugin:react-hooks/recommended',
        'plugin:react/recommended',
        'plugin:react/jsx-runtime',
        'prettier'
      )
    ),

    plugins: {
      'react-refresh': reactRefresh,
      '@typescript-eslint': fixupPluginRules(typescriptEslint),
      prettier,
      eslintConfigPrettier,
    },

    rules: {
      'react-refresh/only-export-components': [
        'warn',
        {
          allowConstantExport: true,
        },
      ],

      'prettier/prettier': 'error',
      '@typescript-eslint/no-explicit-any': 'off',

      '@typescript-eslint/no-unused-vars': [
        'warn',
        {
          argsIgnorePattern: '^_',
          varsIgnorePattern: '^_',
        },
      ],

      'react/prop-types': 'off',
      'react/react-in-jsx-scope': 'off',
    },

    settings: {
      react: {
        version: 'detect',
      },
    },
  },
  globalIgnores(['**/dist', '*.config.**']),
]);
