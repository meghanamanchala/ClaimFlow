import { computed, onMounted, ref } from 'vue';
import { getMe } from '../services/api';

export function useNavbarProfile() {
  const profile = ref(null);

  const displayName = computed(() => {
    const rawName = (profile.value?.name || '').trim();
    if (rawName) {
      return rawName;
    }

    const email = profile.value?.email || '';
    return email ? email.split('@')[0] : 'My Profile';
  });

  const avatarInitials = computed(() => {
    const source = displayName.value;
    const words = source
      .split(/\s+/)
      .filter(Boolean)
      .slice(0, 2);

    const initials = words.map((word) => word.charAt(0).toUpperCase()).join('');
    return initials || 'U';
  });

  async function loadProfile() {
    try {
      const { data } = await getMe();
      profile.value = data;
    } catch {
      profile.value = null;
    }
  }

  onMounted(loadProfile);

  return {
    displayName,
    avatarInitials,
    loadProfile,
  };
}
