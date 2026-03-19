import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface GamificationResult {
  new_level: number
  new_total_xp: number
}

interface UserState {
  userId: string
  username: string
  level: number
  totalXp: number
  streakDays: number
  previousLevel: number
  completedChallengeIds: string[]
  badges: string[]
  dakiLevel: 1 | 2 | 3   // nivel evolutivo de DAKI (sincronizado con el backend)
  setUser: (_user: {
    id: string
    username: string
    current_level: number
    total_xp: number
    streak_days: number
  }) => void
  applyGamificationResult: (_result: GamificationResult) => void
  markChallengeCompleted: (_id: string) => void
  earnBadge: (_badge: string) => void
  setDakiLevel: (_level: 1 | 2 | 3) => void
  clearUser: () => void
}

export const useUserStore = create<UserState>()(
  persist(
    (set) => ({
      userId: '',
      username: '',
      level: 1,
      totalXp: 0,
      streakDays: 0,
      previousLevel: 1,
      completedChallengeIds: [],
      badges: [],
      dakiLevel: 1,

      setUser: ({ id, username, current_level, total_xp, streak_days }) =>
        set({
          userId: id,
          username,
          level: current_level,
          totalXp: total_xp,
          streakDays: streak_days,
          previousLevel: current_level,
        }),

      applyGamificationResult: ({ new_level, new_total_xp }) =>
        set((state) => ({
          previousLevel: state.level,
          level: new_level,
          totalXp: new_total_xp,
        })),

      markChallengeCompleted: (id: string) =>
        set((state) => ({
          completedChallengeIds: state.completedChallengeIds.includes(id)
            ? state.completedChallengeIds
            : [...state.completedChallengeIds, id],
        })),

      earnBadge: (badge: string) =>
        set((state) => ({
          badges: state.badges.includes(badge)
            ? state.badges
            : [...state.badges, badge],
        })),

      setDakiLevel: (level: 1 | 2 | 3) => set({ dakiLevel: level }),

      clearUser: () =>
        set({
          userId: '',
          username: '',
          level: 1,
          totalXp: 0,
          streakDays: 0,
          previousLevel: 1,
          completedChallengeIds: [],
          badges: [],
          dakiLevel: 1,
        }),
    }),
    {
      name: 'pq-user',
      partialize: (state) => ({
        userId:                state.userId,
        username:              state.username,
        level:                 state.level,
        totalXp:               state.totalXp,
        streakDays:            state.streakDays,
        completedChallengeIds: state.completedChallengeIds,
        badges:                state.badges,
        dakiLevel:             state.dakiLevel,
      }),
    }
  )
)
