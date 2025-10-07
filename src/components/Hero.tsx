import heroImage from "@/assets/hero-renewable-energy.jpg";

const Hero = () => {
  return (
    <div className="relative min-h-[600px] flex items-center justify-center overflow-hidden">
      <div 
        className="absolute inset-0 bg-cover bg-center"
        style={{ backgroundImage: `url(${heroImage})` }}
      >
        <div className="absolute inset-0 bg-gradient-to-b from-black/50 via-black/30 to-background" />
      </div>
      
      <div className="relative z-10 container mx-auto px-4 text-center">
        <h1 className="text-5xl md:text-7xl font-bold text-white mb-6 drop-shadow-2xl">
          Power Your Future with
          <span className="block bg-gradient-to-r from-emerald-400 to-sky-400 bg-clip-text text-transparent">
            Smart Renewable Energy
          </span>
        </h1>
        <p className="text-xl md:text-2xl text-white/90 mb-8 max-w-3xl mx-auto drop-shadow-lg">
          AI-powered recommendations for solar, wind, and hybrid systems tailored to your location and energy needs
        </p>
        <div className="flex gap-4 justify-center">
          <div className="bg-white/10 backdrop-blur-sm px-6 py-3 rounded-full border border-white/20">
            <p className="text-white font-semibold">🌍 Geo-Intelligent Analysis</p>
          </div>
          <div className="bg-white/10 backdrop-blur-sm px-6 py-3 rounded-full border border-white/20">
            <p className="text-white font-semibold">⚡ Cost & Savings Calculator</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Hero;
