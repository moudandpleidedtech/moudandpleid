from fastapi import APIRouter

from app.api.v1.endpoints import activity, admin, analytics, boss, bounty, certificate, challenges, compiler, daki, duels, evaluate, gamification, health, hint, intercept, knowledge, leaderboard, payments, sectors, simulate, telemetry, users

router = APIRouter(prefix="/api/v1")

router.include_router(health.router)
router.include_router(admin.router, tags=["admin"])
router.include_router(gamification.router, prefix="/gamification", tags=["gamification"])
router.include_router(compiler.router, tags=["compiler"])
router.include_router(evaluate.router, tags=["evaluate"])
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
router.include_router(certificate.router, tags=["certificate"])
router.include_router(intercept.router)
router.include_router(payments.router, tags=["payments"])
router.include_router(daki.router, tags=["daki"])
router.include_router(knowledge.router, tags=["knowledge"])
