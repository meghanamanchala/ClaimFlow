export const SAMPLE_CLAIMS = [
  {
    id: 1,
    claimNumber: 'CLM-2026-000001',
    userId: 3,
    policyId: 1,
    policyNumber: 'POL-2026-0001',
    claimType: 'Auto',
    incidentDate: '2026-03-01',
    estimatedAmount: 4200,
    status: 'under_review',
    priority: 'medium',
    description: 'Front bumper damage',
    createdAt: '2026-03-02T08:00:00Z',
    documents: [
      {
        fileName: 'invoice.pdf',
        fileType: 'PDF',
        fileUrl: '/uploads/claim_1/invoice.pdf',
        size: 1.2,
        uploadedAt: '2026-03-02T10:00:00Z'
      }
    ],
    timeline: [
      { step: 'Claim Submitted', date: '2026-03-02T08:00:00Z' },
      { step: 'Under Agent Review', date: '2026-03-02T09:00:00Z' }
    ],
    agentId: 2,
    agentNotes: 'Need one more receipt'
  }
];

const USERS = [
  {
    id: 1,
    name: 'Admin User',
    email: 'admin@example.com',
    role: 'admin',
    status: 'active',
    isOnline: true,
    lastLogin: '2026-03-03T09:00:00Z',
    createdAt: '2026-03-01T09:00:00Z'
  },
  {
    id: 2,
    name: 'Agent User',
    email: 'agent@example.com',
    role: 'agent',
    status: 'active',
    isOnline: true,
    lastLogin: '2026-03-03T09:00:00Z',
    createdAt: '2026-03-01T09:00:00Z'
  },
  {
    id: 3,
    name: 'Policyholder User',
    email: 'policyholder@example.com',
    role: 'policyholder',
    status: 'active',
    isOnline: false,
    lastLogin: '2026-03-03T09:00:00Z',
    createdAt: '2026-03-01T09:00:00Z'
  }
];

const POLICIES = [
  {
    id: 1,
    policy_number: 'POL-2026-0001',
    coverage_amount: 12000,
    user_id: 3
  }
];

const PERMISSIONS = {
  roles: [
    {
      role: 'Policyholder',
      items: [
        { name: 'View own claims', enabled: true },
        { name: 'Submit new claims', enabled: true }
      ]
    },
    {
      role: 'Agent',
      items: [
        { name: 'View assigned claims', enabled: true },
        { name: 'Review & update status', enabled: true }
      ]
    },
    {
      role: 'Administrator',
      items: [
        { name: 'Full system access', enabled: true },
        { name: 'Manage users', enabled: true }
      ]
    }
  ]
};

const SETTINGS = {
  general: {
    companyName: 'ClaimFlow Inc.',
    supportEmail: 'support@claimflow.com'
  },
  notifications: {
    emailNotificationsForNewClaims: true,
    smsAlertsForStatusUpdates: false,
    dailySummaryReports: true,
    agentAssignmentNotifications: true
  },
  claimProcessing: {
    autoAssignThreshold: 5000,
    reviewDeadlineDays: 7,
    autoAssignment: true
  }
};

export async function attachApiMocks(page, role = 'policyholder') {
  await page.route('**/*', async (route) => {
    const url = new URL(route.request().url());
    const method = route.request().method();

    if (url.origin !== 'http://127.0.0.1:8000') {
      await route.continue();
      return;
    }

    if (url.pathname === '/login' && method === 'POST') {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ access_token: 'test-token', token_type: 'bearer' })
      });
      return;
    }

    if (url.pathname === '/register' && method === 'POST') {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ message: 'User Registered Successfully' })
      });
      return;
    }

    if (url.pathname === '/me' && method === 'GET') {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          id: role === 'admin' ? 1 : role === 'agent' ? 2 : 3,
          name: `${role} user`,
          email: `${role}@example.com`,
          role
        })
      });
      return;
    }

    if (url.pathname === '/me' && method === 'PUT') {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          id: role === 'admin' ? 1 : role === 'agent' ? 2 : 3,
          name: `${role} user updated`,
          email: `${role}@example.com`,
          role
        })
      });
      return;
    }

    if (url.pathname === '/claims' && method === 'GET') {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify(SAMPLE_CLAIMS)
      });
      return;
    }

    if (url.pathname === '/claims' && method === 'POST') {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ ...SAMPLE_CLAIMS[0], status: 'submitted' })
      });
      return;
    }

    if (url.pathname.match(/^\/claims\/\d+$/) && method === 'GET') {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify(SAMPLE_CLAIMS[0])
      });
      return;
    }

    if (url.pathname.match(/^\/claims\/\d+\/decision$/) && method === 'PATCH') {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ ...SAMPLE_CLAIMS[0], status: 'approved' })
      });
      return;
    }

    if (url.pathname.match(/^\/claims\/\d+\/documents\/upload$/) && method === 'POST') {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify(SAMPLE_CLAIMS[0])
      });
      return;
    }

    if (url.pathname.match(/^\/claims\/\d+\/documents$/) && method === 'DELETE') {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ ...SAMPLE_CLAIMS[0], documents: [] })
      });
      return;
    }

    if (url.pathname === '/policies' && method === 'GET') {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify(POLICIES)
      });
      return;
    }

    if (url.pathname === '/users' && method === 'GET') {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify(USERS)
      });
      return;
    }

    if (url.pathname.match(/^\/admin\/users\/\d+\/status$/) && method === 'PATCH') {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify(USERS[1])
      });
      return;
    }

    if (url.pathname === '/admin/permissions') {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify(PERMISSIONS)
      });
      return;
    }

    if (url.pathname === '/admin/settings') {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify(SETTINGS)
      });
      return;
    }

    if (url.pathname === '/messages' && method === 'GET') {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify([
          {
            id: 1,
            claimId: 1,
            senderId: 2,
            receiverId: 3,
            senderName: 'Agent User',
            content: 'Please upload one more document.',
            createdAt: '2026-03-03T08:00:00Z'
          }
        ])
      });
      return;
    }

    if (url.pathname === '/messages' && method === 'POST') {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          id: 2,
          claimId: 1,
          senderId: role === 'agent' ? 2 : 3,
          receiverId: role === 'agent' ? 3 : 2,
          senderName: role === 'agent' ? 'Agent User' : 'Policyholder User',
          content: 'Acknowledged',
          createdAt: '2026-03-03T09:00:00Z'
        })
      });
      return;
    }

    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({})
    });
  });
}

export async function seedAuth(page, role) {
  await page.addInitScript((seededRole) => {
    localStorage.setItem('claimflow_token', 'test-token');
    localStorage.setItem('claimflow_role', seededRole);
  }, role);
}
