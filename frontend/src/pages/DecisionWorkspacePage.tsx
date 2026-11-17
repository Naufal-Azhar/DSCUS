import { useParams } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { getDecision } from '@/lib/api'
import { Loader2 } from 'lucide-react'

export default function DecisionWorkspacePage() {
  const { id } = useParams<{ id: string }>()
  
  const { data: decision, isLoading, error } = useQuery({
    queryKey: ['decision', id],
    queryFn: () => getDecision(id!),
    enabled: !!id,
  })

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <Loader2 className="w-8 h-8 animate-spin text-blue-600" />
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-red-600 mb-2">Error</h2>
          <p className="text-gray-600">Failed to load decision</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          {decision?.title}
        </h1>
        
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <h2 className="text-xl font-semibold mb-4">Original Context</h2>
          <p className="text-gray-700 whitespace-pre-wrap">
            {decision?.original_input}
          </p>
        </div>

        <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
          <p className="text-blue-800">
            Decision workspace is under construction. 
            Next steps: Add decomposition, graph visualization, and scenario testing.
          </p>
        </div>
      </div>
    </div>
  )
}
