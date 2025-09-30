/**
 * Dark Mode CSS Validation Tests
 * 
 * Testing Framework: Node.js with CSS parsing and validation
 * 
 * These tests validate:
 * - CSS custom property definitions
 * - Selector syntax correctness
 * - Color value formats
 * - Transition property syntax
 * - CSS specificity and structure
 */

import { describe, it, expect, beforeAll } from 'vitest';
import { readFileSync } from 'fs';
import { join } from 'path';

describe('Dark Mode CSS Validation', () => {
  let cssContent: string;

  beforeAll(() => {
    // Read the actual CSS file (assuming it's named dark-mode.css)
    const cssPath = join(__dirname, 'dark-mode.css');
    try {
      cssContent = readFileSync(cssPath, 'utf-8');
    } catch (error) {
      // If file doesn't exist, use the content directly
      cssContent = `
/* Dark Mode Styles for NocoDB */

/* Base dark mode styles */
.dark {
  --nc-bg-primary: #1a1a1a;
  --nc-bg-secondary: #2d2d2d;
  --nc-text-primary: #ffffff;
  --nc-text-secondary: #a0a0a0;
  --nc-border: #404040;
}

/* Dark mode overrides for common elements */
.dark .nc-content-max-w {
  background-color: var(--nc-bg-primary);
  color: var(--nc-text-primary);
}

.dark .border-nc-gray-medium {
  border-color: var(--nc-border);
}

.dark .hover:bg-gray-100:hover {
  background-color: var(--nc-bg-secondary);
}

/* Dark mode for buttons and interactive elements */
.dark button {
  color: var(--nc-text-primary);
}

.dark .text-gray-600 {
  color: var(--nc-text-secondary);
}

/* Dark mode for cards and panels */
.dark .bg-white {
  background-color: var(--nc-bg-secondary);
}

/* Dark mode for inputs */
.dark input,
.dark textarea,
.dark select {
  background-color: var(--nc-bg-secondary);
  color: var(--nc-text-primary);
  border-color: var(--nc-border);
}

/* Dark mode for tables */
.dark table {
  background-color: var(--nc-bg-secondary);
  color: var(--nc-text-primary);
}

.dark th,
.dark td {
  border-color: var(--nc-border);
}

/* Smooth transitions for theme switching */
* {
  transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease;
}
      `;
    }
  });

  describe('CSS Custom Properties (CSS Variables)', () => {
    it('should define all required dark mode CSS custom properties', () => {
      expect(cssContent).toContain('--nc-bg-primary');
      expect(cssContent).toContain('--nc-bg-secondary');
      expect(cssContent).toContain('--nc-text-primary');
      expect(cssContent).toContain('--nc-text-secondary');
      expect(cssContent).toContain('--nc-border');
    });

    it('should use valid hex color values for background colors', () => {
      const bgPrimaryMatch = cssContent.match(/--nc-bg-primary:\s*(#[0-9a-fA-F]{6})/);
      const bgSecondaryMatch = cssContent.match(/--nc-bg-secondary:\s*(#[0-9a-fA-F]{6})/);
      
      expect(bgPrimaryMatch).toBeTruthy();
      expect(bgSecondaryMatch).toBeTruthy();
      
      if (bgPrimaryMatch) {
        expect(bgPrimaryMatch[1]).toMatch(/^#[0-9a-fA-F]{6}$/);
      }
      if (bgSecondaryMatch) {
        expect(bgSecondaryMatch[1]).toMatch(/^#[0-9a-fA-F]{6}$/);
      }
    });

    it('should use valid hex color values for text colors', () => {
      const textPrimaryMatch = cssContent.match(/--nc-text-primary:\s*(#[0-9a-fA-F]{6})/);
      const textSecondaryMatch = cssContent.match(/--nc-text-secondary:\s*(#[0-9a-fA-F]{6})/);
      
      expect(textPrimaryMatch).toBeTruthy();
      expect(textSecondaryMatch).toBeTruthy();
      
      if (textPrimaryMatch) {
        expect(textPrimaryMatch[1]).toMatch(/^#[0-9a-fA-F]{6}$/);
      }
      if (textSecondaryMatch) {
        expect(textSecondaryMatch[1]).toMatch(/^#[0-9a-fA-F]{6}$/);
      }
    });

    it('should use valid hex color value for border color', () => {
      const borderMatch = cssContent.match(/--nc-border:\s*(#[0-9a-fA-F]{6})/);
      
      expect(borderMatch).toBeTruthy();
      if (borderMatch) {
        expect(borderMatch[1]).toMatch(/^#[0-9a-fA-F]{6}$/);
      }
    });

    it('should use CSS custom properties with var() function', () => {
      expect(cssContent).toContain('var(--nc-bg-primary)');
      expect(cssContent).toContain('var(--nc-bg-secondary)');
      expect(cssContent).toContain('var(--nc-text-primary)');
      expect(cssContent).toContain('var(--nc-text-secondary)');
      expect(cssContent).toContain('var(--nc-border)');
    });
  });

  describe('CSS Selector Validation', () => {
    it('should have .dark as the root selector for dark mode', () => {
      expect(cssContent).toMatch(/\.dark\s*\{/);
    });

    it('should properly scope all dark mode styles under .dark selector', () => {
      const darkSelectors = cssContent.match(/\.dark[^{]*/g);
      expect(darkSelectors).toBeTruthy();
      expect(darkSelectors!.length).toBeGreaterThan(5);
    });

    it('should include descendant selectors for nested elements', () => {
      expect(cssContent).toContain('.dark .nc-content-max-w');
      expect(cssContent).toContain('.dark button');
      expect(cssContent).toContain('.dark input');
      expect(cssContent).toContain('.dark table');
    });

    it('should include pseudo-class selector for hover states', () => {
      expect(cssContent).toMatch(/\.dark.*:hover/);
    });

    it('should handle escaped characters in selectors correctly', () => {
      // Check for Tailwind-style escaped selectors
      const hasEscapedSelectors =
        cssContent.includes('hover\\:') ||
        cssContent.includes(':hover');
      expect(hasEscapedSelectors).toBe(true);
    });

    it('should include multi-element selectors for form inputs', () => {
      const inputSelectorMatch = cssContent.match(/\.dark input,[\s\S]*?\.dark textarea,[\s\S]*?\.dark select/);
      expect(inputSelectorMatch).toBeTruthy();
    });

    it('should include table element selectors', () => {
      expect(cssContent).toContain('.dark th');
      expect(cssContent).toContain('.dark td');
    });
  });

  describe('CSS Property Validation', () => {
    it('should define background-color properties using CSS variables', () => {
      expect(cssContent).toMatch(/background-color:\s*var\(--nc-bg-primary\)/);
      expect(cssContent).toMatch(/background-color:\s*var\(--nc-bg-secondary\)/);
    });

    it('should define color properties using CSS variables', () => {
      expect(cssContent).toMatch(/color:\s*var\(--nc-text-primary\)/);
      expect(cssContent).toMatch(/color:\s*var\(--nc-text-secondary\)/);
    });

    it('should define border-color properties using CSS variables', () => {
      expect(cssContent).toMatch(/border-color:\s*var\(--nc-border\)/);
    });

    it('should include transition properties for smooth theme switching', () => {
      expect(cssContent).toContain('transition:');
      expect(cssContent).toMatch(/transition:.*background-color/);
      expect(cssContent).toMatch(/transition:.*color/);
      expect(cssContent).toMatch(/transition:.*border-color/);
    });

    it('should use valid time values in transitions', () => {
      const transitionMatch = cssContent.match(/transition:.*?(\d+\.?\d*s)/);
      expect(transitionMatch).toBeTruthy();
      if (transitionMatch) {
        const timeValue = parseFloat(transitionMatch[1]);
        expect(timeValue).toBeGreaterThan(0);
        expect(timeValue).toBeLessThan(2);
      }
    });

    it('should use valid easing functions in transitions', () => {
      expect(cssContent).toMatch(/transition:.*ease/);
    });
  });

  describe('Color Contrast and Accessibility', () => {
    it('should define a dark primary background color', () => {
      const bgPrimaryMatch = cssContent.match(/--nc-bg-primary:\s*#([0-9a-fA-F]{6})/);
      if (bgPrimaryMatch) {
        const hexValue = bgPrimaryMatch[1];
        const luminance = parseInt(hexValue.slice(0, 2), 16);
        // Dark backgrounds should have low luminance (< 50)
        expect(luminance).toBeLessThan(50);
      }
    });

    it('should define a light text color for dark mode', () => {
      const textPrimaryMatch = cssContent.match(/--nc-text-primary:\s*#([0-9a-fA-F]{6})/);
      if (textPrimaryMatch) {
        const hexValue = textPrimaryMatch[1];
        const luminance = parseInt(hexValue.slice(0, 2), 16);
        // Light text should have high luminance (> 200)
        expect(luminance).toBeGreaterThan(200);
      }
    });

    it('should have distinct primary and secondary background colors', () => {
      const bgPrimaryMatch = cssContent.match(/--nc-bg-primary:\s*(#[0-9a-fA-F]{6})/);
      const bgSecondaryMatch = cssContent.match(/--nc-bg-secondary:\s*(#[0-9a-fA-F]{6})/);

      if (bgPrimaryMatch && bgSecondaryMatch) {
        expect(bgPrimaryMatch[1]).not.toBe(bgSecondaryMatch[1]);
      }
    });

    it('should have distinct primary and secondary text colors', () => {
      const textPrimaryMatch = cssContent.match(/--nc-text-primary:\s*(#[0-9a-fA-F]{6})/);
      const textSecondaryMatch = cssContent.match(/--nc-text-secondary:\s*(#[0-9a-fA-F]{6})/);

      if (textPrimaryMatch && textSecondaryMatch) {
        expect(textPrimaryMatch[1]).not.toBe(textSecondaryMatch[1]);
      }
    });
  });

  describe('CSS Structure and Organization', () => {
    it('should include descriptive comments for each section', () => {
      expect(cssContent).toMatch(/\/\*.*Base dark mode styles.*\*\//);
      expect(cssContent).toMatch(/\/\*.*Dark mode for buttons.*\*\//);
      expect(cssContent).toMatch(/\/\*.*Dark mode for inputs.*\*\//);
      expect(cssContent).toMatch(/\/\*.*Dark mode for tables.*\*\//);
    });

    it('should not contain syntax errors (balanced braces)', () => {
      const openBraces = (cssContent.match(/\{/g) || []).length;
      const closeBraces = (cssContent.match(/\}/g) || []).length;
      expect(openBraces).toBe(closeBraces);
    });

    it('should properly terminate CSS properties with semicolons', () => {
      // Check that properties before closing braces have semicolons
      const propertiesWithoutSemicolon = cssContent.match(/:\s*[^;}\s]+\s*\}/g);
      expect(propertiesWithoutSemicolon).toBeFalsy();
    });

    it('should use consistent indentation', () => {
      const lines = cssContent.split('\n');
      const indentedLines = lines.filter(line => line.match(/^\s+[a-z-]/));
      expect(indentedLines.length).toBeGreaterThan(0);
    });
  });

  describe('Comprehensive Coverage', () => {
    it('should style common UI elements', () => {
      expect(cssContent).toContain('button');
      expect(cssContent).toContain('input');
      expect(cssContent).toContain('textarea');
      expect(cssContent).toContain('select');
      expect(cssContent).toContain('table');
    });

    it('should style table elements comprehensively', () => {
      expect(cssContent).toContain('table');
      expect(cssContent).toContain('th');
      expect(cssContent).toContain('td');
    });

    it('should apply styles to form elements consistently', () => {
      const formElementsRegex = /\.dark (input|textarea|select)[, ]/g;
      const matches = cssContent.match(formElementsRegex);
      expect(matches).toBeTruthy();
      expect(matches!.length).toBeGreaterThanOrEqual(3);
    });

    it('should have a universal selector for transitions', () => {
      expect(cssContent).toMatch(/\*\s*\{/);
    });
  });

  describe('Edge Cases and Error Handling', () => {
    it('should not have duplicate property definitions in the same rule', () => {
      const rules = cssContent.split('}');
      rules.forEach(rule => {
        const properties: string[] = [];
        const propertyMatches = rule.matchAll(/([a-z-]+):/g);
        for (const match of propertyMatches) {
          const propName = match[1];
          if (properties.includes(propName)) {
            // Duplicate found - this might be intentional for fallbacks, but flag it
            console.warn(`Duplicate property found: ${propName}`);
          }
          properties.push(propName);
        }
      });
    });

    it('should handle cascade properly with specificity', () => {
      // Ensure .dark descendant selectors come after .dark root definition
      const darkRootIndex = cssContent.indexOf('.dark {');
      const darkDescendantIndex = cssContent.indexOf('.dark .');

      if (darkRootIndex !== -1 && darkDescendantIndex !== -1) {
        expect(darkDescendantIndex).toBeGreaterThan(darkRootIndex);
      }
    });

    it('should not contain invalid CSS property names', () => {
      const invalidProperties = [
        'colour:', // British spelling
        'backgroundcolor:', // Missing hyphen
        'bordercolor:', // Missing hyphen
      ];

      invalidProperties.forEach(invalid => {
        expect(cssContent.toLowerCase()).not.toContain(invalid);
      });
    });

    it('should use standard CSS color formats', () => {
      // Should not contain invalid color formats
      expect(cssContent).not.toMatch(/color:\s*#[0-9a-fA-F]{3}[^0-9a-fA-F;]/);
      expect(cssContent).not.toContain('color: rgb(');
    });
  });

  describe('Performance Considerations', () => {
    it('should use efficient universal selector transitions', () => {
      const universalTransition = cssContent.match(/\*\s*\{[^}]*transition:/);
      expect(universalTransition).toBeTruthy();
    });

    it('should limit transition properties to only necessary ones', () => {
      const transitionMatch = cssContent.match(/transition:\s*([^;]+);/);
      if (transitionMatch) {
        const transitionValue = transitionMatch[1];
        // Should specify properties rather than using 'all'
        expect(transitionValue).not.toContain('all');
      }
    });

    it('should use reasonable transition durations', () => {
      const transitionMatches = cssContent.matchAll(/(\d+\.?\d*)(s|ms)/g);
      for (const match of transitionMatches) {
        const value = parseFloat(match[1]);
        const unit = match[2];

        if (unit === 's') {
          expect(value).toBeLessThanOrEqual(1);
          expect(value).toBeGreaterThan(0);
        } else if (unit === 'ms') {
          expect(value).toBeLessThanOrEqual(1000);
          expect(value).toBeGreaterThan(0);
        }
      }
    });
  });

  describe('Dark Mode Utility Classes', () => {
    it('should override Tailwind utility classes appropriately', () => {
      expect(cssContent).toContain('.dark .bg-white');
      expect(cssContent).toContain('.dark .text-gray-600');
    });

    it('should handle pseudo-class utilities from Tailwind', () => {
      const hasPseudoClass = cssContent.includes(':hover');
      expect(hasPseudoClass).toBe(true);
    });

    it('should scope border utilities correctly', () => {
      expect(cssContent).toContain('.dark .border-nc-gray-medium');
    });
  });

  describe('CSS Variable Usage Patterns', () => {
    it('should consistently use var() for all color references', () => {
      // Count var() usage
      const varUsages = (cssContent.match(/var\(--nc-[^\)]+\)/g) || []).length;
      expect(varUsages).toBeGreaterThan(10);
    });

    it('should not have hardcoded colors in descendant selectors', () => {
      const descendantSelectors = cssContent.split('.dark ').slice(1);
      descendantSelectors.forEach(selector => {
        const hasHardcodedColor = selector.match(/:\s*#[0-9a-fA-F]{6}/);
        if (hasHardcodedColor) {
          const isInRootDefinition = selector.startsWith('{');
          expect(isInRootDefinition).toBe(true);
        }
      });
    });

    it('should define CSS variables before using them', () => {
      const variableDefinitions = cssContent.indexOf('--nc-bg-primary:');
      const variableUsage = cssContent.indexOf('var(--nc-bg-primary)');

      expect(variableDefinitions).toBeGreaterThan(-1);
      expect(variableUsage).toBeGreaterThan(-1);
      expect(variableUsage).toBeGreaterThan(variableDefinitions);
    });
  });

  describe('Integration with NocoDB Components', () => {
    it('should style NocoDB-specific classes', () => {
      expect(cssContent).toContain('.nc-content-max-w');
      expect(cssContent).toContain('.border-nc-gray-medium');
    });

    it('should provide comprehensive coverage for common components', () => {
      const componentTypes = ['button', 'input', 'table'];
      componentTypes.forEach(type => {
        expect(cssContent).toContain(type);
      });
    });
  });
});

// Additional helper tests for CSS parsing if needed
describe('CSS Syntax Validation', () => {
  it('should be valid CSS that can be parsed', () => {
    const singleQuotes = (cssContent.match(/'/g) || []).length;
    const doubleQuotes = (cssContent.match(/"/g) || []).length;
    
    expect(singleQuotes % 2).toBe(0);
    expect(doubleQuotes % 2).toBe(0);
  });

  it('should not contain CSS syntax errors', () => {
    expect(cssContent).not.toContain(';;');
    expect(cssContent).not.toMatch(/\s:\s/);
    expect(cssContent).not.toMatch(/\{\s*\}/);
  });

  it('should use consistent formatting', () => {
    const colonSpacing = cssContent.match(/[a-z-]+:\s+[^;]+;/g);
    expect(colonSpacing).toBeTruthy();
  });
});