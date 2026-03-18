from fastapi import APIRouter

from app.api.v1.endpoints import activity, analytics, boss, bounty, challenges, compiler, duels, gamification, health, hint, leaderboard, sectors, simulate, telemetry, users

router = APIRouter(prefix="/api/v1")

router.include_router(health.router)
router.include_router(gamification.router, prefix="/gamification", tags=["gamification"])
router.include_router(compiler.router, tags=["compiler"])
router.include_router(challenges.router, tags=["challenges"])
router.include_router(sectors.router, tags=["sectors"])
router.include_router(telemetry.router, tags=["telemetry"])
router.include_router(users.router, tags=["users"])
router.include_router(simulate.router, tags=["simulate"])
router.include_router(hint.router, tags=["hint"])
router.include_router(analytics.router, tags=["analytics"])
router.include_router(boss.router, tags=["boss"])
router.include_router(leaderboard.router, tags=["leaderboard"])
router.include_router(duels.router)
router.include_router(activity.router)
router.include_router(bounty.router)
