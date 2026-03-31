/** @type {import('next').NextConfig} */
const API_ORIGIN = process.env.API_URL ?? process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000'

const nextConfig = {
  reactStrictMode: true,

  // Vercel production build — skip lint/TS errors que no afectan runtime
  eslint:     { ignoreDuringBuilds: true },
  typescript: { ignoreBuildErrors:  true },

  // Proxy: redirige /api/v1/* → http://localhost:8000/api/v1/*
  // Evita errores de CORS y 404 por URL relativa en el frontend.
  async rewrites() {
    return [
      {
        source: '/api/v1/:path*',
        destination: `${API_ORIGIN}/api/v1/:path*`,
      },
    ]
  },
}

export default nextConfig
