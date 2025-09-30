<script lang="ts" setup>
const props = defineProps<{
  workspaceId?: string
}>()

const navigateToWorkspace = () => {
  if (props.workspaceId) {
    navigateTo(`/${props.workspaceId}/settings`)
  }
}

// Dark mode functionality
const isDarkMode = ref(false)

// Check for saved theme preference or default to light mode
onMounted(() => {
  const savedTheme = localStorage.getItem('nc-theme')
  if (savedTheme === 'dark' || (!savedTheme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    isDarkMode.value = true
    document.documentElement.classList.add('dark')
  }
})

// Toggle dark mode
const toggleDarkMode = () => {
  isDarkMode.value = !isDarkMode.value

  if (isDarkMode.value) {
    document.documentElement.classList.add('dark')
    localStorage.setItem('nc-theme', 'dark')
  } else {
    document.documentElement.classList.remove('dark')
    localStorage.setItem('nc-theme', 'light')
  }
}
</script>

<template>
  <div class="flex items-center justify-between w-full border-b-1 border-nc-gray-medium py-2 px-4 h-[56px]">
    <GeneralIcon icon="nocodbSquarePuck" class="w-8 h-8 cursor-pointer" @click.stop="navigateToWorkspace" />

    <div class="flex items-center gap-3">
      <!-- Dark Mode Toggle -->
      <button
        @click="toggleDarkMode"
        class="flex items-center justify-center w-8 h-8 rounded-md hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors duration-200"
        :title="isDarkMode ? 'Switch to light mode' : 'Switch to dark mode'"
      >
        <Transition name="icon-fade" mode="out-in">
          <GeneralIcon v-if="isDarkMode" icon="sun" class="w-5 h-5 text-yellow-500" key="sun" />
          <GeneralIcon v-else icon="moon" class="w-5 h-5 text-gray-600 dark:text-gray-300" key="moon" />
        </Transition>
      </button>

      <DashboardTopbarUserInfo />
    </div>
  </div>
</template>
