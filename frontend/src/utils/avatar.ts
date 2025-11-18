/**
 * Utility functions for avatar fallback based on gender and role
 */

export type Gender = 'male' | 'female' | 'other' | null | undefined
export type Role = 'admin' | 'instructor' | 'student'

/**
 * Get default avatar path based on gender and role
 * @param gender - User's gender ('male', 'female', 'other', or null/undefined)
 * @param role - User's role ('admin', 'instructor', 'student')
 * @returns Path to default avatar image
 */
export function getDefaultAvatar(gender: Gender, role?: Role): string {
  // If no gender specified, use default based on role
  if (!gender || gender === 'other') {
    if (role === 'admin') {
      return '/admin.webp'
    }
    // Default fallback for teacher/student without gender
    return role === 'instructor' 
      ? '/teacherboy.webp' 
      : '/boy.webp'
  }

  // Gender-based avatars
  if (gender === 'male') {
    return role === 'instructor' ? '/teacherboy.webp' : '/boy.webp'
  }
  
  if (gender === 'female') {
    return role === 'instructor' ? '/teachergirl.webp' : '/girl.webp'
  }

  // Fallback
  return role === 'admin' ? '/admin.webp' : '/boy.webp'
}

/**
 * Get avatar source with fallback logic
 * @param userAvatar - User's uploaded avatar URL (if any)
 * @param gender - User's gender
 * @param role - User's role
 * @returns Avatar URL to display
 */
export function getAvatarSrc(
  userAvatar: string | null | undefined,
  gender: Gender,
  role?: Role
): string {
  // If user has uploaded avatar, use it
  if (userAvatar) {
    // Handle base64 data URLs
    if (userAvatar.startsWith('data:')) {
      return userAvatar
    }
    // Handle full URLs
    if (userAvatar.startsWith('http://') || userAvatar.startsWith('https://')) {
      return userAvatar
    }
    // Handle relative paths
    return userAvatar
  }

  // Use default avatar based on gender and role
  return getDefaultAvatar(gender, role)
}

