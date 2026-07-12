import { createRouter, createWebHistory } from 'vue-router';
import LoginView from '../views/auth/LoginView.vue';
import RegisterView from '../views/auth/RegisterView.vue';
import PolicyholderLayout from '../layouts/PolicyholderLayout.vue';
import DashboardView from '../views/policyholder/DashboardView.vue';
import SubmitClaimView from '../views/policyholder/SubmitClaimView.vue';
import MyClaimsView from '../views/policyholder/MyClaimsView.vue';
import DocumentsView from '../views/policyholder/DocumentsView.vue';
import ClaimHistoryView from '../views/policyholder/ClaimHistoryView.vue';
import ProfileView from '../views/shared/ProfileView.vue';
import NotificationsView from '../views/shared/NotificationsView.vue';
import AgentLayout from '../layouts/AgentLayout.vue';
import AgentDashboardView from '../views/agent/AgentDashboardView.vue';
import AssignedClaimsView from '../views/agent/AssignedClaimsView.vue';
import ReviewClaimsView from '../views/agent/ReviewClaimsView.vue';
import AgentMessagesView from '../views/agent/AgentMessagesView.vue';
import AdminLayout from '../layouts/AdminLayout.vue';
import AdminDashboardView from '../views/admin/AdminDashboardView.vue';
import AdminAllClaimsView from '../views/admin/AdminAllClaimsView.vue';
import AdminUserManagementView from '../views/admin/AdminUserManagementView.vue';
import AdminAnalyticsView from '../views/admin/AdminAnalyticsView.vue';
import AdminPermissionsView from '../views/admin/AdminPermissionsView.vue';
import AdminSettingsView from '../views/admin/AdminSettingsView.vue';

function getStoredRole() {
  return localStorage.getItem('claimflow_role');
}

function getRoleHomePath(role) {
  if (role === 'agent') {
    return '/agent/dashboard';
  }

  if (role === 'admin') {
    return '/admin/dashboard';
  }

  if (role === 'policyholder') {
    return '/dashboard';
  }

  return '/login';
}

const routes = [
  {
    path: '/',
    redirect: () => getRoleHomePath(getStoredRole())
  },
  {
    path: '/',
    component: PolicyholderLayout,
    meta: {
      requiresAuth: true,
      allowedRoles: ['policyholder']
    },
    children: [
      {
        path: 'dashboard',
        name: 'dashboard',
        component: DashboardView
      },
      {
        path: 'submit-claim',
        name: 'submit-claim',
        component: SubmitClaimView
      },
      {
        path: 'my-claims',
        name: 'my-claims',
        component: MyClaimsView
      },
      {
        path: 'documents',
        name: 'documents',
        component: DocumentsView
      },
      {
        path: 'claim-history',
        name: 'claim-history',
        component: ClaimHistoryView
      },
      {
        path: 'profile',
        name: 'profile',
        component: ProfileView
      },
      {
        path: 'notifications',
        name: 'notifications',
        component: NotificationsView
      }
    ]
  },
  {
    path: '/login',
    name: 'login',
    meta: {
      public: true
    },
    component: LoginView
  },
  {
    path: '/register',
    name: 'register',
    meta: {
      public: true
    },
    component: RegisterView
  },
  {
    path: '/agent',
    component: AgentLayout,
    meta: {
      requiresAuth: true,
      allowedRoles: ['agent']
    },
    children: [
      {
        path: '',
        redirect: '/agent/dashboard'
      },
      {
        path: 'dashboard',
        name: 'agent-dashboard',
        component: AgentDashboardView
      },
      {
        path: 'assigned-claims',
        name: 'agent-assigned-claims',
        component: AssignedClaimsView
      },
      {
        path: 'review-claims',
        name: 'agent-review-claims',
        component: ReviewClaimsView
      },
      {
        path: 'messages',
        name: 'agent-messages',
        component: AgentMessagesView
      },
      {
        path: 'profile',
        name: 'agent-profile',
        component: ProfileView
      },
      {
        path: 'notifications',
        name: 'agent-notifications',
        component: NotificationsView
      }
    ]
  },
  {
    path: '/admin',
    component: AdminLayout,
    meta: {
      requiresAuth: true,
      allowedRoles: ['admin']
    },
    children: [
      {
        path: '',
        redirect: '/admin/dashboard'
      },
      {
        path: 'dashboard',
        name: 'admin-dashboard',
        component: AdminDashboardView
      },
      {
        path: 'all-claims',
        name: 'admin-all-claims',
        component: AdminAllClaimsView
      },
      {
        path: 'user-management',
        name: 'admin-user-management',
        component: AdminUserManagementView
      },
      {
        path: 'analytics',
        name: 'admin-analytics',
        component: AdminAnalyticsView
      },
      {
        path: 'permissions',
        name: 'admin-permissions',
        component: AdminPermissionsView
      },
      {
        path: 'settings',
        name: 'admin-settings',
        component: AdminSettingsView
      },
      {
        path: 'profile',
        name: 'admin-profile',
        component: ProfileView
      },
      {
        path: 'notifications',
        name: 'admin-notifications',
        component: NotificationsView
      }
    ]
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: () => getRoleHomePath(getStoredRole())
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

router.beforeEach((to) => {
  const token = localStorage.getItem('claimflow_token');
  const role = getStoredRole();

  if (to.meta.public) {
    if (token && role) {
      return getRoleHomePath(role);
    }

    return true;
  }

  if (to.meta.requiresAuth && !token) {
    return '/login';
  }

  const allowedRoles = to.matched.flatMap((record) => record.meta.allowedRoles || []);

  if (allowedRoles.length > 0 && !allowedRoles.includes(role)) {
    if (!token || !role) {
      return '/login';
    }

    return getRoleHomePath(role);
  }

  return true;
});

export default router;
