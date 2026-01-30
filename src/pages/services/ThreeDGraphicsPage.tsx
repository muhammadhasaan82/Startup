import React from 'react';
import { ServiceDetail } from '../../components/ServiceDetail';
import { useLanguage } from '../../contexts/LanguageContext';

export const ThreeDGraphicsPage: React.FC = () => {
    const { t } = useLanguage();
    const serviceData = {
        title: '3D Graphics Designing',
        subtitle: 'Transform Ideas into Stunning 3D Visuals',
        description: 'Bring your concepts to life with professional 3D modeling, rendering, and animation services. From product visualization to architectural rendering, we create photorealistic 3D graphics that captivate and engage.',
        image: 'https://images.unsplash.com/photo-1633356122544-f134324a6cee?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHwzZCUyMGdyYXBoaWNzfGVufDF8fHx8MTczODI0NTYwMHww&ixlib=rb-4.1.0&q=80&w=1080',
        features: [
            '3D Modeling & Sculpting',
            'Product Visualization',
            'Architectural Rendering',
            'Character Design & Rigging',
            'Animation & Motion Graphics',
            'Texturing & Materials',
            'Lighting & Rendering',
            'VFX & Compositing',
            'AR/VR Content Creation',
            'Game Asset Development',
            'Medical & Scientific Visualization',
            'Industrial Design Rendering',
        ],
        benefits: [
            'Photorealistic Quality',
            'Faster Prototyping & Iteration',
            'Cost-Effective Marketing Materials',
            'Enhanced Customer Engagement',
            'Unlimited Creative Possibilities',
            'Professional Industry-Standard Output',
        ],
        process: [
            { title: 'Concept & Planning', description: 'Understand your vision, gather references, and create initial concept sketches' },
            { title: 'Modeling & Sculpting', description: 'Build detailed 3D models using industry-leading software like Blender, Maya, or 3ds Max' },
            { title: 'Texturing & Lighting', description: 'Apply realistic materials, textures, and set up professional lighting for your scenes' },
            { title: 'Rendering & Delivery', description: 'Produce high-quality renders and deliver in your preferred format with revisions' },
        ],
        packages: [
            {
                name: 'Basic 3D Package',
                price: '$599',
                features: [
                    'Simple 3D Model',
                    'Basic Texturing',
                    'Standard Lighting',
                    '2-3 Render Angles',
                    'HD Resolution (1920x1080)',
                    '2 Revisions',
                    '5-7 Day Delivery',
                ],
            },
            {
                name: 'Professional 3D Package',
                price: '$1,299',
                popular: true,
                features: [
                    'Complex 3D Model',
                    'Advanced Texturing & Materials',
                    'Professional Lighting Setup',
                    '5-7 Render Angles',
                    '4K Resolution',
                    'Basic Animation (10-15 sec)',
                    '4 Revisions',
                    '10-14 Day Delivery',
                    'Source Files Included',
                ],
            },
            {
                name: 'Premium 3D Package',
                price: '$2,999',
                features: [
                    'Multiple Complex Models',
                    'Photorealistic Rendering',
                    'Advanced Animation (30-60 sec)',
                    'Unlimited Render Angles',
                    '8K Resolution',
                    'VFX & Compositing',
                    'Interactive 3D Viewer',
                    'Unlimited Revisions',
                    'Priority Support',
                    'Full Source Files & Assets',
                ],
            },
        ],
        faqs: [
            {
                question: 'What software do you use for 3D graphics?',
                answer: 'We use industry-standard software including Blender, Autodesk Maya, 3ds Max, Cinema 4D, ZBrush, and Substance Painter to ensure the highest quality results.',
            },
            {
                question: 'How long does a typical 3D project take?',
                answer: 'Project timelines vary based on complexity. Simple models can be completed in 5-7 days, while complex scenes with animation may take 2-4 weeks. We provide detailed timelines during consultation.',
            },
            {
                question: 'Can you create 3D models from photos or sketches?',
                answer: 'Yes! We can create accurate 3D models from reference photos, technical drawings, sketches, or even physical objects using photogrammetry techniques.',
            },
            {
                question: 'What file formats do you deliver?',
                answer: 'We deliver in all common formats including FBX, OBJ, STL, GLTF, and native project files. We also provide high-resolution renders in PNG, JPEG, or TIFF formats.',
            },
            {
                question: 'Do you offer 3D printing preparation services?',
                answer: 'Absolutely! We can optimize 3D models for 3D printing, ensuring proper geometry, wall thickness, and export in STL or other 3D printing formats.',
            },
        ],
    };

    return <ServiceDetail {...serviceData} />;
};
