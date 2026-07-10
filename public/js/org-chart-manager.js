/**
 * Organization Chart Manager
 * Handles loading, saving, and managing org hierarchy
 */

class OrgChartManager {
  constructor() {
    this.data = null;
    this.storageKey = 'sojpe_org_chart';
    this.configPath = './config/org-chart.json';
  }

  /**
   * Load org chart from storage or file
   */
  async load() {
    // First, try to load from localStorage
    const cached = localStorage.getItem(this.storageKey);
    if (cached) {
      try {
        this.data = JSON.parse(cached);
        console.log('✓ Org chart loaded from localStorage');
        return this.data;
      } catch (e) {
        console.warn('Failed to parse cached org chart, loading from file');
      }
    }

    // Fall back to loading from file
    try {
      const response = await fetch(this.configPath);
      this.data = await response.json();
      console.log('✓ Org chart loaded from file');
      return this.data;
    } catch (error) {
      console.error('Failed to load org chart:', error);
      throw new Error('Unable to load organization hierarchy');
    }
  }

  /**
   * Save org chart to localStorage
   */
  save() {
    if (!this.data) {
      throw new Error('No data to save');
    }

    // Update timestamp
    this.data.lastUpdated = new Date().toISOString();

    try {
      localStorage.setItem(this.storageKey, JSON.stringify(this.data));
      console.log('✓ Org chart saved to localStorage');
      return true;
    } catch (error) {
      console.error('Failed to save org chart:', error);
      throw new Error('Unable to save organization hierarchy');
    }
  }

  /**
   * Get all members
   */
  getAll() {
    return this.data?.organization || [];
  }

  /**
   * Get member by ID
   */
  getById(id) {
    return this.data?.organization.find(m => m.id === id);
  }

  /**
   * Get all directors
   */
  getDirectors() {
    return this.data?.organization.filter(m => m.level === 'director' && m.active) || [];
  }

  /**
   * Get members by director
   */
  getByDirector(directorId) {
    return this.data?.organization.filter(m => m.parent === directorId && m.active) || [];
  }

  /**
   * Get org hierarchy tree structure
   */
  getTree() {
    const directors = this.getDirectors();
    return directors.map(director => ({
      ...director,
      members: this.getByDirector(director.id)
    }));
  }

  /**
   * Get for dashboard display
   */
  getDashboardData() {
    return this.getTree();
  }

  /**
   * Add new member
   */
  addMember(member) {
    if (!this.data) {
      throw new Error('Org chart not loaded');
    }

    // Validate required fields
    if (!member.id || !member.name || !member.title) {
      throw new Error('Member must have id, name, and title');
    }

    // Check for duplicate ID
    if (this.data.organization.some(m => m.id === member.id)) {
      throw new Error(`Member with ID ${member.id} already exists`);
    }

    // Add with defaults
    const newMember = {
      active: true,
      email: '',
      notes: '',
      ...member,
      created: new Date().toISOString()
    };

    this.data.organization.push(newMember);
    this.save();
    return newMember;
  }

  /**
   * Update existing member
   */
  updateMember(id, updates) {
    if (!this.data) {
      throw new Error('Org chart not loaded');
    }

    const member = this.data.organization.find(m => m.id === id);
    if (!member) {
      throw new Error(`Member with ID ${id} not found`);
    }

    Object.assign(member, updates, { modified: new Date().toISOString() });
    this.save();
    return member;
  }

  /**
   * Delete member
   */
  deleteMember(id) {
    if (!this.data) {
      throw new Error('Org chart not loaded');
    }

    const index = this.data.organization.findIndex(m => m.id === id);
    if (index === -1) {
      throw new Error(`Member with ID ${id} not found`);
    }

    // Mark as inactive instead of deleting (soft delete)
    this.data.organization[index].active = false;
    this.data.organization[index].modified = new Date().toISOString();
    this.save();
    return true;
  }

  /**
   * Validate org structure
   */
  validate() {
    if (!this.data?.organization) {
      return { valid: false, errors: ['No organization data'] };
    }

    const errors = [];
    const ids = new Set();

    // Check for duplicate IDs and missing required fields
    this.data.organization.forEach((member, index) => {
      if (ids.has(member.id)) {
        errors.push(`Duplicate ID at row ${index + 1}: ${member.id}`);
      }
      ids.add(member.id);

      if (!member.name) {
        errors.push(`Missing name at row ${index + 1}`);
      }
      if (!member.title) {
        errors.push(`Missing title at row ${index + 1}`);
      }
      if (!member.level) {
        errors.push(`Missing level at row ${index + 1}`);
      }
    });

    // Check for orphaned members (parent doesn't exist)
    this.data.organization.forEach((member, index) => {
      if (member.parent && !ids.has(member.parent)) {
        errors.push(`Invalid parent ID at row ${index + 1}: ${member.parent}`);
      }
    });

    return {
      valid: errors.length === 0,
      errors,
      memberCount: this.data.organization.filter(m => m.active).length
    };
  }

  /**
   * Export as JSON
   */
  exportJSON() {
    return JSON.stringify(this.data, null, 2);
  }

  /**
   * Export as CSV
   */
  exportCSV() {
    const members = this.data?.organization || [];
    const headers = ['ID', 'Name', 'Title', 'Level', 'Portfolio', 'Reports To', 'Email', 'Active'];
    const rows = members.map(m => [
      m.id,
      m.name,
      m.title,
      m.level,
      m.portfolio,
      m.parent || '—',
      m.email,
      m.active ? 'Yes' : 'No'
    ]);

    const csv = [headers, ...rows].map(row => row.map(cell => `"${cell}"`).join(',')).join('\n');
    return csv;
  }

  /**
   * Import from JSON
   */
  importJSON(jsonString) {
    try {
      const imported = JSON.parse(jsonString);
      if (!imported.organization || !Array.isArray(imported.organization)) {
        throw new Error('Invalid JSON format');
      }
      this.data = imported;
      this.save();
      return this.validate();
    } catch (error) {
      throw new Error(`Import failed: ${error.message}`);
    }
  }

  /**
   * Get summary stats
   */
  getSummary() {
    const all = this.getAll();
    const active = all.filter(m => m.active);
    const directors = active.filter(m => m.level === 'director');
    const ams = active.filter(m => m.level === 'account_manager');
    const aads = active.filter(m => m.level === 'associate_director');

    return {
      totalMembers: active.length,
      directors: directors.length,
      accountManagers: ams.length,
      associateDirectors: aads.length,
      lastUpdated: this.data?.lastUpdated
    };
  }

  /**
   * Clear all data and reset to defaults
   */
  resetToDefaults() {
    localStorage.removeItem(this.storageKey);
    this.data = null;
    console.log('✓ Org chart reset to defaults');
  }
}

// Create global instance
window.orgChartManager = new OrgChartManager();
