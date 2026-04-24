import type { MetadataRoute } from 'next'
import { getAllPosts } from '@/lib/posts'

export default function sitemap(): MetadataRoute.Sitemap {
  const posts = getAllPosts()

  const postEntries: MetadataRoute.Sitemap = posts.map((post) => ({
    url:              `https://dakiedtech.com/blog/${post.slug}`,
    lastModified:     new Date(post.publishedAt),
    changeFrequency:  'monthly',
    priority:         0.7,
  }))

  return [
    {
      url:             'https://dakiedtech.com',
      lastModified:    new Date(),
      changeFrequency: 'weekly',
      priority:        1,
    },
    {
      url:             'https://dakiedtech.com/blog',
      lastModified:    new Date(),
      changeFrequency: 'weekly',
      priority:        0.9,
    },
    ...postEntries,
    {
      url:             'https://dakiedtech.com/comunidad',
      lastModified:    new Date(),
      changeFrequency: 'daily',
      priority:        0.8,
    },
    {
      url:             'https://dakiedtech.com/plataforma',
      lastModified:    new Date(),
      changeFrequency: 'monthly',
      priority:        0.85,
    },
    {
      url:             'https://dakiedtech.com/precios',
      lastModified:    new Date(),
      changeFrequency: 'monthly',
      priority:        0.85,
    },
    {
      url:             'https://dakiedtech.com/register',
      lastModified:    new Date(),
      changeFrequency: 'monthly',
      priority:        0.8,
    },
    {
      url:             'https://dakiedtech.com/login',
      lastModified:    new Date(),
      changeFrequency: 'yearly',
      priority:        0.5,
    },
    {
      url:             'https://dakiedtech.com/privacidad',
      lastModified:    new Date(),
      changeFrequency: 'yearly',
      priority:        0.3,
    },
  ]
}
