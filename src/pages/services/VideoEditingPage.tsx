import React from 'react';
import { ServiceDetail } from '../../components/ServiceDetail';
import { useLanguage } from '../../contexts/LanguageContext';

export const VideoEditingPage: React.FC = () => {
    const { t } = useLanguage();
    const serviceData = {
        title: 'Video Editing',
        subtitle: 'Create Engaging Content That Captivates',
        description: 'Professional video editing services that transform raw footage into compelling stories. From corporate videos to social media content, we deliver polished, engaging videos that resonate with your audience.',
        image: 'https://images.unsplash.com/photo-1574717024653-61fd2cf4d44d?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHx2aWRlbyUyMGVkaXRpbmd8ZW58MXx8fHwxNzM4MjQ1NjAwfDA&ixlib=rb-4.1.0&q=80&w=1080',
        features: [
            'Commercial Video Production',
            'Social Media Content Editing',
            'Color Grading & Correction',
            'Motion Graphics & VFX',
            'Audio Enhancement & Mixing',
            'Subtitle & Caption Creation',
            'Green Screen Compositing',
            'Multi-Camera Editing',
            'YouTube & Vlog Editing',
            'Corporate & Training Videos',
            'Event & Wedding Videos',
            'Promotional & Advertisement Videos',
        ],
        benefits: [
            'Professional Cinematic Quality',
            'Fast Turnaround Times',
            'Engaging Storytelling',
            'Platform-Optimized Formats',
            'Increased Audience Engagement',
            'Brand Consistency & Polish',
        ],
        process: [
            { title: 'Brief & Planning', description: 'Discuss your vision, target audience, and project goals to create a clear editing plan' },
            { title: 'Footage Review', description: 'Analyze raw footage, select best takes, and organize assets for efficient editing' },
            { title: 'Editing & Enhancement', description: 'Cut, arrange, color grade, add effects, motion graphics, and enhance audio' },
            { title: 'Review & Delivery', description: 'Present draft for feedback, implement revisions, and deliver final video in desired formats' },
        ],
        packages: [
            {
                name: 'Social Media Package',
                price: '$399',
                features: [
                    'Up to 3 Minutes Video',
                    'Basic Color Correction',
                    'Simple Transitions',
                    'Background Music',
                    'Text Overlays',
                    '2 Revisions',
                    'Social Media Formats',
                    '3-5 Day Delivery',
                ],
            },
            {
                name: 'Professional Package',
                price: '$899',
                popular: true,
                features: [
                    'Up to 10 Minutes Video',
                    'Advanced Color Grading',
                    'Motion Graphics',
                    'Sound Design & Mixing',
                    'Custom Animations',
                    'Subtitles/Captions',
                    '4 Revisions',
                    'Multiple Format Export',
                    '7-10 Day Delivery',
                ],
            },
            {
                name: 'Premium Package',
                price: '$1,999',
                features: [
                    'Up to 30 Minutes Video',
                    'Cinematic Color Grading',
                    'Advanced VFX & Compositing',
                    'Professional Audio Mastering',
                    'Custom Motion Graphics',
                    'Multi-Language Subtitles',
                    'Green Screen Compositing',
                    'Unlimited Revisions',
                    'Priority Support',
                    'Raw Project Files Included',
                ],
            },
        ],
        faqs: [
            {
                question: 'What video formats do you accept?',
                answer: 'We accept all common video formats including MP4, MOV, AVI, MKV, and professional formats like ProRes and DNxHD. We can work with footage from any camera or device.',
            },
            {
                question: 'How do I send you my footage?',
                answer: 'You can upload footage via cloud services like Google Drive, Dropbox, WeTransfer, or any file-sharing platform. For large projects, we can provide secure FTP access.',
            },
            {
                question: 'Can you add music and sound effects?',
                answer: 'Yes! We have access to extensive royalty-free music and sound effect libraries. You can also provide your own music or we can source licensed tracks based on your preferences.',
            },
            {
                question: 'What is your revision policy?',
                answer: 'Each package includes a specified number of revisions. We provide a draft for your review and implement your feedback. Additional revisions beyond the package limit can be purchased.',
            },
            {
                question: 'Do you offer rush delivery?',
                answer: 'Yes, we offer expedited delivery for an additional fee. Rush projects can typically be completed in 1-3 days depending on complexity and current workload.',
            },
        ],
    };

    return <ServiceDetail {...serviceData} />;
};
