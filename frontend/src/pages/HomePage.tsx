import { Link } from 'react-router-dom'
import { Brain, Target, Zap } from 'lucide-react'

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-16">
        {/* Header */}
        <div className="text-center mb-16">
          <h1 className="text-6xl font-bold text-gray-900 mb-4">
            DecisionMirror
          </h1>
          <p className="text-2xl text-gray-700 mb-8">
            Think Before You Commit.
          </p>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto mb-12">
            Turn your personal decisions into editable reasoning models. 
            Challenge assumptions, explore what-if scenarios, and see how changes 
            affect your thinking.
          </p>
          
          <Link
            to="/new"
            className="inline-block bg-blue-600 hover:bg-blue-700 text-white font-semibold px-8 py-4 rounded-lg text-lg transition-colors shadow-lg"
          >
            Start a Decision
          </Link>
        </div>

        {/* Features */}
        <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto mt-20">
          <div className="bg-white rounded-lg p-6 shadow-md">
            <div className="flex items-center justify-center w-12 h-12 bg-blue-100 rounded-lg mb-4">
              <Brain className="w-6 h-6 text-blue-600" />
            </div>
            <h3 className="text-xl font-semibold mb-2">Decompose</h3>
            <p className="text-gray-600">
              Break down your decision into claims, assumptions, evidence, and alternatives.
            </p>
          </div>

          <div className="bg-white rounded-lg p-6 shadow-md">
            <div className="flex items-center justify-center w-12 h-12 bg-purple-100 rounded-lg mb-4">
              <Target className="w-6 h-6 text-purple-600" />
            </div>
            <h3 className="text-xl font-semibold mb-2">Challenge</h3>
            <p className="text-gray-600">
              Review AI-generated counterarguments and see which assumptions are critical.
            </p>
          </div>

          <div className="bg-white rounded-lg p-6 shadow-md">
            <div className="flex items-center justify-center w-12 h-12 bg-green-100 rounded-lg mb-4">
              <Zap className="w-6 h-6 text-green-600" />
            </div>
            <h3 className="text-xl font-semibold mb-2">Stress Test</h3>
            <p className="text-gray-600">
              Change assumptions and see which claims and consequences are affected.
            </p>
          </div>
        </div>

        {/* Use Cases */}
        <div className="mt-20 max-w-3xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-8">Perfect for</h2>
          <ul className="space-y-3 text-lg text-gray-700">
            <li className="flex items-start">
              <span className="text-blue-600 mr-2">•</span>
              <span>Deciding whether to accept an internship in another city</span>
            </li>
            <li className="flex items-start">
              <span className="text-blue-600 mr-2">•</span>
              <span>Choosing whether to change your university major</span>
            </li>
            <li className="flex items-start">
              <span className="text-blue-600 mr-2">•</span>
              <span>Evaluating whether to buy expensive equipment for studies or work</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  )
}
