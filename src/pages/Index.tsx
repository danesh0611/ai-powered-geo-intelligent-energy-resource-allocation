import { useState } from "react";
import Hero from "@/components/Hero";
import EnergyForm from "@/components/EnergyForm";
import ResultsDashboard from "@/components/ResultsDashboard";
import { useToast } from "@/hooks/use-toast";

const Index = () => {
  const [results, setResults] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const { toast } = useToast();

  const handleFormSubmit = async (formData: any) => {
    setIsLoading(true);
    
    try {
      // Connect to our Python backend
      const response = await fetch("http://localhost:5000/api/recommend", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        throw new Error("Failed to get recommendations");
      }

      const data = await response.json();
      setResults(data);
      
      toast({
        title: "Analysis Complete!",
        description: "Your personalized recommendations are ready.",
      });

      // Scroll to results
      setTimeout(() => {
        document.getElementById("results")?.scrollIntoView({ behavior: "smooth" });
      }, 100);
    } catch (error) {
      console.error("Error:", error);
      toast({
        title: "Connection Error",
        description: "Make sure your Python backend is running on port 5000",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background">
      <Hero />
      
      <div className="container mx-auto px-4 py-16">
        <EnergyForm onSubmit={handleFormSubmit} isLoading={isLoading} />
      </div>

      {results && (
        <div id="results" className="container mx-auto px-4 pb-16">
          <ResultsDashboard data={results} />
        </div>
      )}
    </div>
  );
};

export default Index;
