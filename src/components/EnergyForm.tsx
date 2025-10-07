import { useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { MapPin, Zap, Building2, IndianRupee } from "lucide-react";

interface EnergyFormData {
  location: string;
  usageType: "home" | "factory" | "agriculture";
  monthlyConsumption: number;
  tariff?: number; // Optional now as we use slabs
  budget?: number;
  slabs?: {
    slab1Rate?: number; // 0-100 kWh
    slab2Rate?: number; // 101-300 kWh
    slab3Rate?: number; // 301-500 kWh
    slab4Rate?: number; // >500 kWh
  };
}

interface EnergyFormProps {
  onSubmit: (data: EnergyFormData) => void;
  isLoading?: boolean;
}

const EnergyForm = ({ onSubmit, isLoading }: EnergyFormProps) => {
  const [formData, setFormData] = useState<EnergyFormData>({
    location: "",
    usageType: "home",
    monthlyConsumption: 0,
    tariff: 0,
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <Card className="w-full max-w-2xl mx-auto shadow-[var(--shadow-elegant)]">
      <CardHeader>
        <CardTitle className="text-2xl flex items-center gap-2">
          <Zap className="text-primary" />
          Energy Assessment Form
        </CardTitle>
        <CardDescription>
          Enter your details to get personalized renewable energy recommendations
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="space-y-2">
            <Label htmlFor="location" className="flex items-center gap-2">
              <MapPin className="w-4 h-4" />
              Location
            </Label>
            <Input
              id="location"
              placeholder="e.g., Chennai, Tamil Nadu"
              value={formData.location}
              onChange={(e) => setFormData({ ...formData, location: e.target.value })}
              required
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="usageType" className="flex items-center gap-2">
              <Building2 className="w-4 h-4" />
              Usage Type
            </Label>
            <Select
              value={formData.usageType}
              onValueChange={(value: "home" | "factory" | "agriculture") =>
                setFormData({ ...formData, usageType: value })
              }
            >
              <SelectTrigger id="usageType">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="home">Home</SelectItem>
                <SelectItem value="factory">Factory</SelectItem>
                <SelectItem value="agriculture">Agriculture</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2">
            <Label htmlFor="consumption">
              Monthly Consumption (kWh)
            </Label>
            <Input
              id="consumption"
              type="number"
              placeholder="450"
              value={formData.monthlyConsumption || ""}
              onChange={(e) =>
                setFormData({ ...formData, monthlyConsumption: Number(e.target.value) })
              }
              required
            />
          </div>
          
          <div className="space-y-4">
            <Label className="flex items-center gap-2">
              <IndianRupee className="w-4 h-4" />
              Electricity Tariff Slabs
            </Label>
            
            <div className="grid gap-3">
              <div className="grid grid-cols-2 gap-3">
                <div className="space-y-2">
                  <Label htmlFor="slab1Rate" className="text-sm">
                    Slab 1 Rate (₹/unit, 0-100 kWh)
                  </Label>
                  <Input
                    id="slab1Rate"
                    type="number"
                    step="0.1"
                    placeholder="4.0"
                    value={formData.slabs?.slab1Rate || ""}
                    onChange={(e) =>
                      setFormData({ 
                        ...formData, 
                        slabs: { 
                          ...(formData.slabs || {}), 
                          slab1Rate: Number(e.target.value) 
                        } 
                      })
                    }
                  />
                </div>
                
                <div className="space-y-2">
                  <Label htmlFor="slab2Rate" className="text-sm">
                    Slab 2 Rate (₹/unit, 101-300 kWh)
                  </Label>
                  <Input
                    id="slab2Rate"
                    type="number"
                    step="0.1"
                    placeholder="6.0"
                    value={formData.slabs?.slab2Rate || ""}
                    onChange={(e) =>
                      setFormData({ 
                        ...formData, 
                        slabs: { 
                          ...(formData.slabs || {}), 
                          slab2Rate: Number(e.target.value) 
                        } 
                      })
                    }
                  />
                </div>
              </div>
              
              <div className="grid grid-cols-2 gap-3">
                <div className="space-y-2">
                  <Label htmlFor="slab3Rate" className="text-sm">
                    Slab 3 Rate (₹/unit, 301-500 kWh)
                  </Label>
                  <Input
                    id="slab3Rate"
                    type="number"
                    step="0.1"
                    placeholder="8.0"
                    value={formData.slabs?.slab3Rate || ""}
                    onChange={(e) =>
                      setFormData({ 
                        ...formData, 
                        slabs: { 
                          ...(formData.slabs || {}), 
                          slab3Rate: Number(e.target.value) 
                        } 
                      })
                    }
                  />
                </div>
                
                <div className="space-y-2">
                  <Label htmlFor="slab4Rate" className="text-sm">
                    Slab 4 Rate (₹/unit, &gt;500 kWh)
                  </Label>
                  <Input
                    id="slab4Rate"
                    type="number"
                    step="0.1"
                    placeholder="10.0"
                    value={formData.slabs?.slab4Rate || ""}
                    onChange={(e) =>
                      setFormData({ 
                        ...formData, 
                        slabs: { 
                          ...(formData.slabs || {}), 
                          slab4Rate: Number(e.target.value) 
                        } 
                      })
                    }
                  />
                </div>
              </div>
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="budget">
              Budget (Optional, ₹)
            </Label>
            <Input
              id="budget"
              type="number"
              placeholder="300000"
              value={formData.budget || ""}
              onChange={(e) =>
                setFormData({ ...formData, budget: Number(e.target.value) || undefined })
              }
            />
          </div>

          <Button
            type="submit"
            className="w-full bg-gradient-to-r from-primary to-accent hover:opacity-90 transition-opacity"
            size="lg"
            disabled={isLoading}
          >
            {isLoading ? "Analyzing..." : "Get AI Recommendations"}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
};

export default EnergyForm;
