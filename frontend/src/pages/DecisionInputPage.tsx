import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useMutation } from '@tanstack/react-query'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { ArrowLeft } from 'lucide-react'
import { Link } from 'react-router-dom'
import { createDecision } from '@/lib/api'

const decisionSchema = z.object({
  title: z.string().min(1, 'Title is required').max(500),
  original_input: z.string().min(10, 'Please provide more context (at least 10 characters)'),
  locale: z.enum(['en', 'id']).default('en'),
})

type DecisionFormData = z.infer<typeof decisionSchema>

export default function DecisionInputPage() {
  const navigate = useNavigate()
  const [locale, setLocale] = useState<'en' | 'id'>('en')

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<DecisionFormData>({
    resolver: zodResolver(decisionSchema),
    defaultValues: {
      locale: 'en',
    },
  })

  const mutation = useMutation({
    mutationFn: createDecision,
    onSuccess: (data) => {
      navigate(`/decision/${data.id}`)
    },
  })

  const onSubmit = (data: DecisionFormData) => {
    mutation.mutate({ ...data, locale })
  }

  const t = locale === 'id' ? {
    title: 'Buat Keputusan Baru',
    backHome: 'Kembali ke Beranda',
    decisionTitle: 'Judul Keputusan',
    decisionTitlePlaceholder: 'Misalnya: Haruskah saya menerima magang di kota lain?',
    decisionContext: 'Konteks & Detail',
    decisionContextPlaceholder: 'Jelaskan situasi Anda, alternatif yang sedang Anda pertimbangkan, dan apa yang Anda tidak yakin...',
    language: 'Bahasa',
    english: 'English',
    indonesian: 'Bahasa Indonesia',
    creating: 'Membuat...',
    createDecision: 'Buat Keputusan',
  } : {
    title: 'Create New Decision',
    backHome: 'Back to Home',
    decisionTitle: 'Decision Title',
    decisionTitlePlaceholder: 'e.g., Should I accept the internship offer in another city?',
    decisionContext: 'Context & Details',
    decisionContextPlaceholder: 'Describe your situation, the alternatives you\'re considering, and what you\'re uncertain about...',
    language: 'Language',
    english: 'English',
    indonesian: 'Bahasa Indonesia',
    creating: 'Creating...',
    createDecision: 'Create Decision',
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8 max-w-3xl">
        <Link
          to="/"
          className="inline-flex items-center text-blue-600 hover:text-blue-700 mb-6"
        >
          <ArrowLeft className="w-4 h-4 mr-2" />
          {t.backHome}
        </Link>

        <h1 className="text-4xl font-bold text-gray-900 mb-8">
          {t.title}
        </h1>

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
          {/* Language Selector */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              {t.language}
            </label>
            <div className="flex gap-4">
              <button
                type="button"
                onClick={() => setLocale('en')}
                className={`px-4 py-2 rounded-md ${
                  locale === 'en'
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                }`}
              >
                {t.english}
              </button>
              <button
                type="button"
                onClick={() => setLocale('id')}
                className={`px-4 py-2 rounded-md ${
                  locale === 'id'
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                }`}
              >
                {t.indonesian}
              </button>
            </div>
          </div>

          {/* Title */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              {t.decisionTitle}
            </label>
            <input
              {...register('title')}
              type="text"
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder={t.decisionTitlePlaceholder}
            />
            {errors.title && (
              <p className="mt-1 text-sm text-red-600">{errors.title.message}</p>
            )}
          </div>

          {/* Context */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              {t.decisionContext}
            </label>
            <textarea
              {...register('original_input')}
              rows={8}
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder={t.decisionContextPlaceholder}
            />
            {errors.original_input && (
              <p className="mt-1 text-sm text-red-600">{errors.original_input.message}</p>
            )}
          </div>

          {/* Submit */}
          <button
            type="submit"
            disabled={mutation.isPending}
            className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-semibold px-6 py-3 rounded-md transition-colors"
          >
            {mutation.isPending ? t.creating : t.createDecision}
          </button>

          {mutation.isError && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-md">
              Failed to create decision. Please try again.
            </div>
          )}
        </form>
      </div>
    </div>
  )
}
