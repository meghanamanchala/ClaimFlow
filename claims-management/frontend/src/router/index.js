import { createRouter, createWebHistory } from 'vue-router';
import LoginView from '../views/LoginView.vue';
import RegisterView from '../views/RegisterView.vue';
import PolicyholderLayout from '../views/PolicyholderLayout.vue';
import DashboardView from '../views/DashboardView.vue';
import SubmitClaimView from '../views/SubmitClaimView.vue';
import MyClaimsView from '../views/MyClaimsView.vue';
import DocumentsView from '../views/DocumentsView.vue';
import ClaimHistoryView from '../views/ClaimHistoryView.vue';
import AgentLayout from '../views/AgentLayout.vue';
import AgentDashboardView from '../views/AgentDashboardView.vue';
import AssignedClaimsView from '../views/AssignedClaimsView.vue';
import ReviewClaimsView from '../views/ReviewClaimsView.vue';
import AgentMessagesView from '../views/AgentMessagesView.vue';
import AdminLayout from '../views/AdminLayout.vue';
import AdminDashboardView from '../views/AdminDashboardView.vue';
import AdminAllClaimsView from '../views/AdminAllClaimsView.vue';
import AdminUserManagementView from '../views/AdminUserManagementView.vue';
import AdminAnalyticsView from '../views/AdminAnalyticsView.vue';
import AdminPermissionsView from '../views/AdminPermissionsView.vue';
import AdminSettingsView from '../views/AdminSettingsView.vue';

const routes = [
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/',
    component: PolicyholderLayout,
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
      }
    ]
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterView
  },
  {
    path: '/agent',
    component: AgentLayout,
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
      }
    ]
  },
  {
    path: '/admin',
    component: AdminLayout,
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
      }
    ]
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
